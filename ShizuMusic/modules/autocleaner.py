import os, time, shutil, asyncio, urllib.parse, random, io, aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

CLEAN_DIRS = ["downloads", "cache", "raw_files", "temp"]
MAX_FILE_AGE = 600  # 10 minutes
TEMP_EXTENSIONS = (".webm", ".mkv", ".mp4", ".mp3", ".m4a", ".part", ".ytdl", ".jpg", ".png", ".ogg")

# 🎨 4K Image API for Storage Report
async def get_cleaner_image():
    prompt = "futuristic cyber girl server room aesthetic glowing 4k"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed={random.randint(100,99999)}&width=1024&height=1024&nologo=true"
    try:
        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    bio = io.BytesIO(await resp.read())
                    bio.name = "cleaner.jpg"
                    return bio
    except: pass
    return url

def clean_old_files():
    now = time.time()
    removed_count, freed_bytes = 0, 0
    
    for folder in CLEAN_DIRS:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        if now - os.path.getmtime(fp) > MAX_FILE_AGE:
                            size = os.path.getsize(fp)
                            os.remove(fp)
                            removed_count += 1
                            freed_bytes += size
                    except: pass
                        
    for f in os.listdir("."):
        if f.endswith(TEMP_EXTENSIONS) and os.path.isfile(f):
            try:
                if now - os.path.getmtime(f) > MAX_FILE_AGE:
                    size = os.path.getsize(f)
                    os.remove(f)
                    removed_count += 1
                    freed_bytes += size
            except: pass
                
    return removed_count, round(freed_bytes / (1024 * 1024), 2)

async def background_auto_cleaner():
    while True:
        try: await asyncio.to_thread(clean_old_files)
        except: pass
        await asyncio.sleep(300) # Runs every 5 minutes

try:
    asyncio.get_event_loop().create_task(background_auto_cleaner())
except: pass

@bot.on_message(filters.command(["clearcache", "clean", "rmdownloads"], prefixes=["/", "!", "."]))
async def manual_clean_cmd(client, message: Message):
    m = await message.reply_text("🧹 **MGB Storage Cleaner kachra saaf kar raha hai...**")
    removed, freed_mb = await asyncio.to_thread(clean_old_files)
    
    total, used, free = shutil.disk_usage("/")
    free_gb = round(free / (1024**3), 2)
    used_percent = round((used / total) * 100, 1)
    
    caption = (
        f"🧹 **MGB VPS AUTO-CLEANER REPORT** 🧹\n\n"
        f"🗑️ **Files Deleted:** `{removed} files`\n"
        f"⚡ **Space Freed:** `{freed_mb} MB`\n"
        f"💾 **VPS Free Disk:** `{free_gb} GB` (`{used_percent}% Used`)\n"
        f"🛡️ **Auto-Guard:** `Active (Every 5 mins)`\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    img = await get_cleaner_image()
    
    try:
        await message.reply_photo(photo=img, caption=caption, reply_markup=kb)
        await m.delete()
    except Exception:
        await m.edit_text(caption, reply_markup=kb)
        
