import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot  # 👈 यहाँ भी हमने सही बॉट इंस्टेंस लगा दिया है

# 6 खूबसूरत वेलकम फ़ोटोज़ (आप चाहें तो इन्हें बदल भी सकते हैं)
WELCOME_IMAGES = [
    "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg",
    "https://files.catbox.moe/ddzvc0.jpg",
    "https://telegra.ph/file/32b0c30953a9cd8ea265a.jpg",
    "https://telegra.ph/file/71f652b415b3c5825cfd3.jpg",
    "https://telegra.ph/file/82633010b9fdb823ddf81.jpg",
    "https://telegra.ph/file/8b1e42817ce8c94622c81.jpg"
]

# जब भी कोई नया मेंबर ग्रुप में आएगा, यह कमांड ऑटोमैटिक ट्रिगर होगा
@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    for member in message.new_chat_members:
        
        # अगर बॉट को ही किसी ने ग्रुप में ऐड किया है, तो यह खुद का स्वागत नहीं करेगा
        if member.id == bot.me.id:
            continue

        random_img = random.choice(WELCOME_IMAGES)
        
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
            await message.reply_photo(
                photo=random_img,
                caption=welcome_text,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Welcome Error: {e}")
            
