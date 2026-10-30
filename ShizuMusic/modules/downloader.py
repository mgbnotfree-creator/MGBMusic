# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#               FAST YT-DLP DOWNLOADER + AUTO CLEAN
# ═══════════════════════════════════════════════════════════════

import os
import time
import asyncio
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot
from ShizuMusic.modules.ai import send_4k_card, get_owner_kb

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_media_sync(query: str, is_audio: bool = False):
    ts = int(time.time())
    outtmpl = os.path.join(DOWNLOAD_DIR, f"mgb_{ts}_%(id)s.%(ext)s")
    search_target = query if query.startswith(("http://", "https://")) else f"ytsearch1:{query}"
    
    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": 50 * 1024 * 1024,
        "geo_bypass": True,
    }
    if is_audio:
        ydl_opts["format"] = "bestaudio/best"
    else:
        ydl_opts["format"] = "best[ext=mp4][height<=720]/best[ext=mp4]/best"
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_target, download=True)
        if "entries" in info:
            info = info["entries"][0]
        file_path = ydl.prepare_filename(info)
        title = info.get("title", "MGB Media")
        return file_path, title

@bot.on_message(filters.command(["dl", "download", "video", "song"], prefixes=["/", "!", "."]))
async def media_downloader(client, message: Message):
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading...**")
        return await send_4k_card(
            message=message,
            status_msg=m,
            prompt_img="anime girl listening to music neon headphones 4k",
            caption=(
                "📥 **MGB ULTRA FAST DOWNLOADER** 📥\n\n"
                "✦ **How to use:**\n"
                "• `/dl [YouTube/Insta Link ya Song Name]`\n"
                "• `/song [Song Name]` (Audio ke liye)\n"
                "• `/video [Video Name/Link]` (Video ke liye)\n\n"
                "💌 Powered by @MGB_NOT_FREE"
            )
        )
        
    cmd = message.command[0].lower()
    is_audio = cmd == "song"
    query = message.text.split(None, 1)[1]
    
    m = await message.reply_text(f"📥 **MGB Downloader `{query}` download kar raha hai...** ⚡")
    file_path = None
    
    try:
        file_path, title = await asyncio.to_thread(download_media_sync, query, is_audio)
        caption = (
            f"🎬 **Title:** `{title[:80]}`\n"
            f"👤 **Requested by:** {message.from_user.mention if message.from_user else 'User'}\n\n"
            f"💌 Powered by @MGB_NOT_FREE"
        )
        if is_audio:
            await message.reply_audio(audio=file_path, caption=caption, title=title[:60], reply_markup=get_owner_kb())
        else:
            await message.reply_video(video=file_path, caption=caption, reply_markup=get_owner_kb())
        await m.delete()
    except Exception as e:
        await send_4k_card(
            message, m,
            "cute anime girl confused 4k",
            f"❌ **Download Error:** `{str(e)[:200]}`\n\n💌 Powered by @MGB_NOT_FREE"
        )
    finally:
        # Instant file cleanup so VPS disk never fills up!
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
                
