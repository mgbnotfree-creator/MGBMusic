import random
import urllib.parse
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🌟 HD AI प्रॉम्प्ट्स (वेलकम के लिए शानदार और खुशमिजाज इमेजेस)
PROMPTS = [
    "beautiful aesthetic anime girl welcoming, 4k resolution, highly detailed",
    "cute anime girl waving hand smiling, cyber neon city, 8k quality, aesthetic",
    "gorgeous anime waifu smiling, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "beautiful anime girl with flowers, extremely detailed, hd"
]

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    for member in message.new_chat_members:
        
        # बॉट खुद का वेलकम नहीं करेगा
        if member.id == bot.me.id:
            continue
            
        # 1. रैंडम प्रॉम्प्ट और सीड चुनकर एक नई HD इमेज जनरेट करें
        prompt = random.choice(PROMPTS)
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        
        # यह जादुई लिंक हर बार 1024x1024 पिक्सल की फुल HD इमेज बनाएगा
        generated_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
        
        welcome_text = (
            f"🎉 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏** 🎉\n\n"
            f"✨ ʜᴇʏ {member.mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ **{message.chat.title}**!\n\n"
            f"💎 **ᴍᴇᴍʙᴇʀ ɪɴғᴏ:**\n"
            f" ├ ɴᴀᴍᴇ: {member.first_name}\n"
            f" ├ ɪᴅ: `{member.id}`\n"
            f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
            f"💌 ᴘᴏᴡᴇʀᴇᴅ ʙʏ : **MGB NOT FREE CODER**"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/RIYA_MUSIC_BOT_786")],
            [InlineKeyboardButton("💬 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫", url="https://t.me/MGB_CODER")]
        ])
        
        try:
            # बॉट नई AI HD फोटो के साथ वेलकम मैसेज भेजेगा
            await message.reply_photo(
                photo=generated_image_url,
                caption=welcome_text,
                reply_markup=keyboard
            )
        except Exception as e:
            # अगर फोटो बनने में टाइम लगा या इंटरनेट स्लो हुआ, तो बिना फोटो के मैसेज भेज देगा
            await message.reply_text(text=welcome_text, reply_markup=keyboard)
            
