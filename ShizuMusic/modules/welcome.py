import random
import urllib.parse
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

async def generate_welcome_image(prompt):
    encoded_prompt = urllib.parse.quote(f"{prompt} highly detailed 4k resolution aesthetic anime greeting")
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
    return f"https://image.pollinations.ai/prompt/cute%20anime%20girl%20welcoming%20aesthetic%204k?width=1280&height=1280&seed={seed}&nologo=true&enhance=true"

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    me = await client.get_me()
    bot_id = me.id
    bot_username = me.username

    for member in message.new_chat_members:
        if member.id == bot_id:
            continue
            
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
            [InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ", url="https://t.me/MGB_CODER"), InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")],
            [InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{bot_username}?startgroup=true")]
        ])
        
        welcome_text = (
            f"🎉 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏 🎉\n\n"
            f"✨ ʜᴇʏ {member.mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {message.chat.title}!\n\n"
            f"💎 ᴍᴇᴍʙᴇʀ ɪɴғᴏ:\n"
            f" ├ ɴᴀᴍᴇ: {member.first_name}\n"
            f" ├ ɪᴅ: {member.id}\n"
            f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
            f"💌 Powered by @MGB_NOT_FREE"
        )
        
        top_img = await generate_welcome_image("cute anime girl welcoming new member")
        try:
            await message.reply_photo(photo=top_img, caption=welcome_text, reply_markup=keyboard)
        except Exception:
            pass
            
