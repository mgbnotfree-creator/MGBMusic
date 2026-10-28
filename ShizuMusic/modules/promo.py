import random
import urllib.parse
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🌟 HD AI प्रॉम्प्ट्स (बॉट इनके आधार पर खुद एकदम नई HD फोटो बनाएगा)
PROMPTS = [
    "beautiful aesthetic anime girl, 4k resolution, highly detailed, masterpiece",
    "cute anime girl in cyber neon city, 8k quality, glowing aesthetic",
    "gorgeous anime waifu, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "anime girl with sword, dark aesthetic, extremely detailed, hd"
]

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]) & filters.user(8853897167))
async def promo_message(client, message: Message):
    
    # 1. रैंडम प्रॉम्प्ट और सीड चुनकर एक नई HD इमेज जनरेट करें
    prompt = random.choice(PROMPTS)
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    
    # यह जादुई लिंक हर बार 1024x1024 पिक्सल की फुल HD इमेज बनाएगा
    generated_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
    
    promo_text = (
        "🎉 **𝐒𝐏𝐄𝐂𝐈𝐀𝐋 𝐏𝐑𝐎𝐌𝐎𝐓𝐈𝐎𝐍** 🎉\n\n"
        "✨ **MGB NOT FREE CODER** ᴋɪ ᴛᴀʀᴀғ sᴇ ʙᴇsᴛ ᴏғғᴇʀs!\n\n"
        "🔥 ᴀɢᴀʀ ᴀᴀᴘᴋᴏ ᴀᴘɴᴀ ᴋʜᴜᴅ ᴋᴀ ᴍᴜsɪᴄ ʙᴏᴛ, ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʏᴀ "
        "ᴋɪsɪ ʙʜɪ ᴛᴀʀᴀʜ ᴋᴀ ᴘʏᴛʜᴏɴ ᴘʀᴏᴊᴇᴄᴛ ʙᴀɴᴡᴀɴᴀ ʜᴀɪ, ᴛᴏʜ ᴀᴀᴊ ʜɪ ᴄᴏɴᴛᴀᴄᴛ ᴋᴀʀᴇɪɴ!\n\n"
        "💎 **ᴏᴜʀ sᴇʀᴠɪᴄᴇs:**\n"
        " ├ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ʙᴏᴛs\n"
        " ├ ᴠᴘs & ʀᴇɴᴅᴇʀ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ\n"
        " └ ᴄᴜsᴛᴏᴍ ᴀᴘɪ & ᴅᴀᴛᴀʙᴀsᴇ sᴇᴛᴜᴘ\n\n"
        "💌 ᴘᴏᴡᴇʀᴇᴅ ʙʏ : **MGB NOT FREE CODER**"
    )
    
    # 🔥 बिल्कुल Aero Music स्टाइल वाला कीबोर्ड (1 Full, 2 Half, 1 Full)
    keyboard = InlineKeyboardMarkup([
        # पहली लाइन: सिंगल बड़ा बटन
        [InlineKeyboardButton("⚡ 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        
        # दूसरी लाइन: दो छोटे बटन एक साथ (Side-by-Side)
        [
            InlineKeyboardButton("👑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ↗", url="https://t.me/MGB_CODER"),
            InlineKeyboardButton("🎁 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ↗", url="https://t.me/RIYA_MUSIC_BOT_786")
        ],
        
        # तीसरी लाइन: ऐड मी बटन
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 ➕", url=f"https://t.me/{bot.me.username}?startgroup=true")]
    ])
    
    try:
        # बॉट नई AI HD फोटो और स्टाइलिश बटन्स के साथ प्रोमो भेजेगा
        await message.reply_photo(
            photo=generated_image_url,
            caption=promo_text,
            reply_markup=keyboard
        )
    except Exception:
        # बैकअप: अगर इंटरनेट स्लो हुआ, तो बिना फोटो के मैसेज भेज देगा
        await message.reply_text(text=promo_text, reply_markup=keyboard)
        
