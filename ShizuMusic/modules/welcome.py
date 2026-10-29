import random
import urllib.parse
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

# 🌟 Premium HD Welcome Prompts
PROMPTS = [
    "beautiful aesthetic anime girl welcoming, 4k resolution, highly detailed",
    "cute anime girl waving hand smiling, cyber neon city, 8k quality, aesthetic",
    "gorgeous anime waifu smiling, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "beautiful anime girl with flowers, extremely detailed, hd"
]

# 🧠 1. SUPERFAST TEXT AI
async def fetch_welcome_text(first_name, chat_title):
    prompt = f"Write a short, aesthetic, and energetic welcome message for user '{first_name}' who joined '{chat_title}'. Keep it under 3 lines. Use emojis like 🎉, ✨, 💎. Write in stylish Hinglish. Do not use bold markdown for the main title."
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

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    me = await client.get_me()
    bot_id = me.id
    bot_username = me.username

    for member in message.new_chat_members:
        # Bot khud ka welcome nahi karega
        if member.id == bot_id:
            continue
            
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
            [
                InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ", url="https://t.me/MGB_CODER"),
                InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")
            ],
            [InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{bot_username}?startgroup=true")]
        ])
        
        # Fetch Custom Welcome Text & Info
        ai_text = await fetch_welcome_text(member.first_name, message.chat.title)
        
        if ai_text:
            welcome_text = (
                f"{ai_text}\n\n"
                f"💎 ᴍᴇᴍʙᴇʀ ɪɴғᴏ:\n"
                f" ├ ɴᴀᴍᴇ: {member.mention}\n"
                f" ├ ɪᴅ: {member.id}\n"
                f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
                f"💌 Powered by @MGB_NOT_FREE"
            )
        else:
            welcome_text = (
                f"🎉 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏 🎉\n\n"
                f"✨ ʜᴇʏ {member.mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {message.chat.title}!\n\n"
                f"💎 ᴍᴇᴍʙᴇʀ ɪɴғᴏ:\n"
                f" ├ ɴᴀᴍᴇ: {member.first_name}\n"
                f" ├ ɪᴅ: {member.id}\n"
                f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
                f"💌 Powered by @MGB_NOT_FREE"
            )
        
        # Fetch Custom Image
        img_url = await fetch_lexica_image(random.choice(PROMPTS))

        # Send Final Message
        try:
            if img_url:
                await message.reply_photo(photo=img_url, caption=welcome_text, reply_markup=keyboard)
            else:
                await message.reply_text(text=welcome_text, reply_markup=keyboard)
        except Exception:
            pass # Welcome mein error aane par group me spam nahi karenge
                                        
