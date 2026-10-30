# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#               VPS STORAGE ANTI-CRASH AUTOCLEANER
# ═══════════════════════════════════════════════════════════════

import os
import time
import shutil
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot
from ShizuMusic.modules.ai import send_4k_card

CLEAN_DIRS = ["downloads", "cache", "raw_files", "temp"]
MAX_FILE_AGE = 600  # 10 minutes (Active songs safe rahenge)
TEMP_EXTENSIONS = (".webm", ".mkv", ".mp4", ".mp3", ".m4a", ".part", ".ytdl", ".jpg", ".png", ".ogg")

def clean_old_files(force_all: bool = False):
    now = time.time()
    removed_count = 0
    freed_bytes = 0
    
    # 1. Clean target folders
    for folder in CLEAN_DIRS:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        file_age = now - os.path.getmtime(fp)
                        if force_all or file_age > MAX_FILE_AGE:
                            size = os.path.getsize(fp)
                            os.remove(fp)
                            removed_count += 1
                            freed_bytes += size
                    except Exception:
                        pass
                        
    # 2. Clean stray media files in root directory
    for f in os.listdir("."):
        if f.endswith(TEMP_EXTENSIONS) and os.path.isfile(f):
            try:
                file_age = now - os.path.getmtime(f)
                if force_all or file_age > MAX_FILE_AGE:
                    size = os.path.getsize(f)
                    os.remove(f)
                    removed_count += 1
                    freed_bytes += size
            except Exception:
                pass
                
    return removed_count, round(freed_bytes / (1024 * 1024), 2)

async def background_auto_cleaner():
    while True:
        try:
            await asyncio.to_thread(clean_old_files, False)
        except Exception:
            pass
        await asyncio.sleep(300)  # Runs every 5 minutes

# Start background loop safely
try:
    loop = asyncio.get_event_loop()
    loop.create_task(background_auto_cleaner())
except Exception:
    pass

@bot.on_message(filters.command(["clearcache", "clean", "rmdownloads"], prefixes=["/", "!", "."]))
async def manual_clean_cmd(client, message: Message):
    m = await message.reply_text("🧹 **MGB Storage Cleaner kachra saaf kar raha hai...**")
    removed, freed_mb = await asyncio.to_thread(clean_old_files, False)
    
    total, used, free = shutil.disk_usage("/")
    free_gb = round(free / (1024**3), 2)
    used_percent = round((used / total) * 100, 1)
    
    report = (
        f"🧹 **MGB VPS AUTO-CLEANER REPORT** 🧹\n\n"
        f"🗑️ **Files Deleted:** `{removed} files`\n"
        f"⚡ **Space Freed:** `{freed_mb} MB`\n"
        f"💾 **VPS Free Disk:** `{free_gb} GB` (`{used_percent}% Used`)\n"
        f"🛡️ **Auto-Guard:** `Active (Every 5 mins)`\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    await send_4k_card(message, m, "futuristic cyber girl server room 4k", report)
    
