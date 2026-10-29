import random
import urllib.parse
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

# 🌟 Premium HD Prompts
PROMPTS = [
    "beautiful aesthetic anime girl, 4k resolution, highly detailed, masterpiece",
    "cute anime girl in cyber neon city, 8k quality, glowing aesthetic",
    "gorgeous anime waifu, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "anime girl with sword, dark aesthetic, extremely detailed, hd"
]

# 🧠 1. SUPERFAST TEXT AI
async def fetch_promo_text():
    prompt = "Write a highly engaging and aesthetic Telegram promotional message for 'MGB NOT FREE CODER'. Highlight services: Premium Music Bots, AI Bots, Render Deployment, and Custom APIs. Use aesthetic emojis, stylish formatting, and professional Hinglish. Keep it concise. Do not use bold markdown for the main title."
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
    except Exception:
        return None
    return None

# 🎨 2. PREMIUM HD IMAGE API (Lexica)
async def fetch_lexica_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://lexica.art/api/v1/search?q={encoded_prompt}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and "images" in data and len(data["images"]) > 0:
                        return random.choice(data["images"][:3])["src"]
    except Exception:
        return None
    return None

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]) & filters.user(8853897167))
async def promo_message(client, message: Message):
    m = await message.reply_text("⏳ **Premium Promo ban raha hai... Please wait!** 🕸️")
    
    me = await client.get_me()
    bot_username = me.username
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        [
            InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ", url="https://t.me/MGB_CODER"),
            InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")
        ],
        [InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{bot_username}?startgroup=true")]
    ])
    
    # Default Fallback Text
    promo_text = (
        "🎉 𝐒𝐏𝐄𝐂𝐈𝐀𝐋 𝐏𝐑𝐎𝐌𝐎𝐓𝐈𝐎𝐍 🎉\n\n"
        "✨ MGB NOT FREE CODER ᴋɪ ᴛᴀʀᴀғ sᴇ ʙᴇsᴛ ᴏғғᴇʀs!\n\n"
        "🔥 ᴀɢᴀʀ ᴀᴀᴘᴋᴏ ᴀᴘɴᴀ ᴋʜᴜᴅ ᴋᴀ ᴍᴜsɪᴄ ʙᴏᴛ, ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʏᴀ "
        "ᴋɪsɪ ʙʜɪ ᴛᴀʀᴀʜ ᴋᴀ ᴘʏᴛʜᴏɴ ᴘʀᴏᴊᴇᴄᴛ ʙᴀɴᴡᴀɴᴀ ʜᴀɪ, ᴛᴏʜ ᴀᴀᴊ ʜɪ ᴄᴏɴᴛᴀᴄᴛ ᴋᴀʀᴇɪɴ!\n\n"
        "💎 ᴏᴜʀ sᴇʀᴠɪᴄᴇs:\n"
        " ├ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ʙᴏᴛs\n"
        " ├ ᴠᴘs & ʀᴇɴᴅᴇʀ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ\n"
        " └ ᴄᴜsᴛᴏᴍ ᴀᴘɪ & ᴅᴀᴛᴀʙᴀsᴇ sᴇᴛᴜᴘ\n\n"
        "💌 Powered by @MGB_NOT_FREE"
    )

    # Fetch AI Text & Image
    ai_text = await fetch_promo_text()
    if ai_text:
        promo_text = f"{ai_text}\n\n💌 Powered by @MGB_NOT_FREE"
        
    img_url = await fetch_lexica_image(random.choice(PROMPTS))

    # Send Final Message
    try:
        if img_url:
            await message.reply_photo(photo=img_url, caption=promo_text, reply_markup=keyboard)
        else:
            await message.reply_text(text=promo_text, reply_markup=keyboard)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
    
