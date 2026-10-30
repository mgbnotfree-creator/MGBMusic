import os
import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot

# ==========================================
# 🧹 ADVANCED MUSIC BOT AUTO-CLEANER ENGINE
# ==========================================

# Music bots jin folders me files save karte hain
CLEAN_DIRECTORIES = ["downloads", "cache", "raw_files"]

# File kitni purani hone par delete karni hai? (600 seconds = 10 minutes)
# Isse jo gaana current play ho raha hai wo delete nahi hoga!
MAX_FILE_AGE = 600  

async def background_auto_cleaner():
    """
    Ye background task har 5 minute mein automatically chalega 
    aur purani files ko chupchap delete kar dega taaki VPS kabhi full na ho.
    """
    while True:
        await asyncio.sleep(300)  # Har 5 minute (300 sec) me check karega
        current_time = time.time()
        
        for directory in CLEAN_DIRECTORIES:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    try:
                        if os.path.isfile(file_path):
                            file_age = os.path.getmtime(file_path)
                            # Agar file 10 minute se zyada purani hai, toh uda do
                            if (current_time - file_age) > MAX_FILE_AGE:
                                os.remove(file_path)
                    except Exception:
                        pass

# 🚀 Bot start hote hi Auto-Cleaner engine ko background me chalu kar do
asyncio.create_task(background_auto_cleaner())


# ==========================================
# 👑 OWNER COMMAND: FORCE CLEAR CACHE & RAM
# ==========================================
@bot.on_message(filters.command(["clearcache", "freeram", "clean"]) & filters.user(8853897167))
async def force_clear_cache(client, message: Message):
    m = await message.reply_text("🧹 **MGB Advanced System Storage Scan kar raha hai...** ⏳")
    
    deleted_files_count = 0
    freed_space_bytes = 0
    
    for directory in CLEAN_DIRECTORIES:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path):
                        # Delete hone se pehle file ka size calculate kar lo
                        freed_space_bytes += os.path.getsize(file_path)
                        os.remove(file_path)
                        deleted_files_count += 1
                except Exception:
                    pass
                    
    # Bytes ko Megabytes (MB) me convert karna
    freed_space_mb = round(freed_space_bytes / (1024 * 1024), 2)
    
    await m.edit_text(
        f"✅ **VPS STORAGE TRICK APPLIED SUCESSFULLY!**\n\n"
        f"🗑️ **Junk Files Deleted:** `{deleted_files_count}`\n"
        f"💾 **Storage Freed:** `{freed_space_mb} MB`\n\n"
        f"🚀 *Aapka server ab bilkul fresh aur fast ho gaya hai!*\n"
        f"💌 **Powered by @MGB_NOT_FREE**"
    )
