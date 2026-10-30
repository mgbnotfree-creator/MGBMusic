import random
import urllib.parse
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

async def generate_promo_image(prompt):
    encoded_prompt = urllib.parse.quote(f"{prompt} highly detailed 4k resolution luxury cyberpunk promo banner")
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
    return f"https://image.pollinations.ai/prompt/cyberpunk%20luxury%20anime%20promo%20banner%204k?width=1280&height=1280&seed={seed}&nologo=true&enhance=true"

@bot.on_message(filters.command("promo"))
async def promo_handler(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_promo_image("vip promotion aesthetic banner")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✨ **Usage:** `/promo <your promotional text>`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
        
    promo_text = " ".join(message.command[1:])
    top_img = await generate_promo_image(promo_text)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")]
    ])
    
    await message.reply_photo(photo=top_img, caption=f"🔥 **MGB VIP PROMOTION ZONE** 🔥\n\n{promo_text}\n\n👑 **Join Now & Enjoy Unlimited Vibe!**\n\n💌 Managed by @MGB_NOT_FREE", reply_markup=keyboard)
    
