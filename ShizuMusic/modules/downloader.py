import os
import shutil
import random
import urllib.parse
import aiohttp
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

async def generate_download_image(prompt):
    encoded_prompt = urllib.parse.quote(f"{prompt} highly detailed 4k resolution music media aesthetic")
    lexica_url = f"https://lexica.art/api/v1/search?q={encoded_prompt}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(lexica_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and "images" in data and len(data["images"]) > 0:
                        return random.choice(data["images"][:5])["src"]
    except Exception:
        pass
    seed = random.randint(1000, 999999)
    return f"https://image.pollinations.ai/prompt/music%20media%20download%20aesthetic%20anime%204k?width=1280&height=1280&seed={seed}&nologo=true&enhance=true"

@bot.on_message(filters.command(["dl", "video", "song"]))
async def download_media(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_download_image("music downloader interface aesthetic")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="📥 **MGB MEDIA DOWNLOADER** 📥\n\n✨ **Usage:** `/dl <YouTube URL>`\n🚀 *Example:* `/dl https://youtu.be/...`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

    url = message.command[1]
    m = await message.reply_text("📥 **Downloading media, please wait...** ⏳")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'geo_bypass': True,
        'nocheckcertificate': True,
        'quiet': True
    }
    file_path = None

    try:
        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Downloaded Media')

        await m.edit_text("📤 **Uploading to Telegram...** 🚀")
        
        top_img = await generate_download_image(title)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
            [InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")]
        ])
        
        await message.reply_photo(photo=top_img, caption=f"✨ **MGB DOWNLOAD ZONE** ✨\n\n🎵 **Title:** `{title}`\n\n❤️ **Powered by @MGB_NOT_FREE**", reply_markup=keyboard)
        
        if file_path and ('mp3' in file_path or 'audio' in url):
            await message.reply_audio(audio=file_path, caption=title)
        else:
            await message.reply_video(video=file_path, caption=title)

        await m.delete()

    except Exception as e:
        await m.edit_text(f"❌ **Download Error:** Video private ho sakti hai ya link galat hai!\n`Error: {e}`")
    
    finally:
        # 🌟 STORAGE FULL TRICK (100% Guaranteed Cleanup) 🌟
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        try:
            if os.path.exists("downloads"):
                shutil.rmtree("downloads")
        except:
            pass
    
