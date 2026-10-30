import io, random, urllib.parse, aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

async def get_promo_image():
    prompt = "stylish anime girl cyberpunk neon luxury music dj 4k"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed={random.randint(100,99999)}&width=1024&height=1024&nologo=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    bio = io.BytesIO(await resp.read())
                    bio.name = "promo.jpg"
                    return bio
    except: pass
    return url

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]))
async def promo_command(client, message: Message):
    m = await message.reply_text("💎 **MGB 4K Promo Banner aa raha hai...** ✨")
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/RIYA_MUSIC_BOT_786"), InlineKeyboardButton("☒ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")]
    ])
    
    caption = (
        "👑 **MGB NOT FREE CODER** 👑\n\n"
        "✨ `Premium Music Bots` 🎶 | `AI Bots` 🤖 | `Render Deployment` 🚀\n\n"
        "💬 Speed, stability aur personalization ka perfect mix!\n"
        "🔗 **DM karein abhi:** 🚀\n\n"
        "🔥 **Your bots, your style — upgrade your game now!**\n\n"
        "💌 Powered by @MGB_NOT_FREE"
    )
    
    img = await get_promo_image()
    try:
        await message.reply_photo(photo=img, caption=caption, reply_markup=keyboard)
        await m.delete()
    except Exception:
        await m.edit_text(caption, reply_markup=keyboard)
        
