import os, time, asyncio, urllib.parse, random, io, aiohttp
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 🎨 4K Image API for Downloader Help Menu
async def get_dl_image():
    prompt = "anime girl listening to music neon headphones 4k aesthetic"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed={random.randint(100,99999)}&width=1024&height=1024&nologo=true"
    try:
        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    bio = io.BytesIO(await resp.read())
                    bio.name = "downloader.jpg"
                    return bio
    except: pass
    return url

def download_media_sync(query: str, is_audio: bool = False):
    ts = int(time.time())
    outtmpl = os.path.join(DOWNLOAD_DIR, f"mgb_{ts}_%(id)s.%(ext)s")
    search_target = query if query.startswith(("http://", "https://")) else f"ytsearch1:{query}"
    
    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": 50 * 1024 * 1024, # 50MB Limit
        "geo_bypass": True,
    }
    ydl_opts["format"] = "bestaudio/best" if is_audio else "best[ext=mp4][height<=720]/best[ext=mp4]/best"
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_target, download=True)
        if "entries" in info: info = info["entries"][0]
        return ydl.prepare_filename(info), info.get("title", "MGB Media")

@bot.on_message(filters.command(["dl", "download", "video", "song"], prefixes=["/", "!", "."]))
async def media_downloader(client, message: Message):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    # Help Menu with 4K Image
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading MGB Downloader...**")
        caption = (
            "📥 **MGB ULTRA FAST DOWNLOADER** 📥\n\n"
            "✦ **How to use:**\n"
            "┠ `/dl [YouTube/Insta Link ya Name]`\n"
            "┠ `/song [Song Name]` (Audio ke liye)\n"
            "┗ `/video [Name/Link]` (Video ke liye)\n\n"
            "💌 Powered by @MGB_NOT_FREE"
        )
        img = await get_dl_image()
        try:
            await message.reply_photo(photo=img, caption=caption, reply_markup=kb)
            await m.delete()
        except Exception:
            await m.edit_text(caption, reply_markup=kb)
        return
        
    cmd = message.command[0].lower()
    is_audio = cmd == "song"
    query = message.text.split(None, 1)[1]
    
    m = await message.reply_text(f"📥 **MGB Downloader `{query}` fetch kar raha hai...** ⚡")
    file_path = None
    
    try:
        file_path, title = await asyncio.to_thread(download_media_sync, query, is_audio)
        caption = f"🎬 **Title:** `{title[:80]}`\n👤 **Requested by:** {message.from_user.mention}\n\n💌 Powered by @MGB_NOT_FREE"
        
        if is_audio: await message.reply_audio(audio=file_path, caption=caption, title=title[:60], reply_markup=kb)
        else: await message.reply_video(video=file_path, caption=caption, reply_markup=kb)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ **Download Error:** `{str(e)[:200]}`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=kb)
    finally:
        if file_path and os.path.exists(file_path):
            try: os.remove(file_path)
            except: pass
    
