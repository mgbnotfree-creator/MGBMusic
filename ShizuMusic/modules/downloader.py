import os
import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp

from ShizuMusic import bot

# 🎯 आपके Boss-style प्रीमियम एस्थेटिक बटन्स
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
    [
        InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ", url="https://t.me/MGB_CODER"),
        InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")
    ]
])

@bot.on_message(filters.command(["dl", "reel", "tiktok", "video"], prefixes=["/", "!", "."]))
async def video_downloader(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ **Boss, koi link toh do!**\nExample: `/dl <video link>`")
    
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("📥 **MGB AI Video Download kar raha hai... Please wait!** 🕸️")
    
    # Download folder setup
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True
    }
    
    try:
        # Background task for downloading video (so bot doesn't hang)
        loop = asyncio.get_event_loop()
        def download_vid():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        
        file_path = await loop.run_in_executor(None, download_vid)
        
        await m.edit_text("📤 **MGB Server se Telegram par upload ho raha hai...** 🚀")
        
        await message.reply_video(
            video=file_path,
            caption=f"🎥 **Video Downloaded Successfully!**\n\n💌 Powered by @MGB_NOT_FREE",
            reply_markup=keyboard
        )
        await m.delete()
        
        # Space bachane ke liye file delete karna
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await m.edit_text(f"❌ **Download Error:** Video private ho sakti hai ya link galat hai!\n_(Error: {e})_")
