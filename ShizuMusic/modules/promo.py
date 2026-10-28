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
    seed = random.randint(1, 1000000) # हर बार एकदम नई फोटो के लिए
    
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
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/RIYA_MUSIC_BOT_786")],
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{bot.me.username}?startgroup=true")]
    ])
    
    try:
        # बॉट टेलीग्राम को वह जनरेटेड इमेज भेजने को कहेगा
        await message.reply_photo(photo=generated_image_url, caption=promo_text, reply_markup=keyboard)
    except Exception as e:
        # बैकअप
        await message.reply_text(text=promo_text, reply_markup=keyboard)
        
