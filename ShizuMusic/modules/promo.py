import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID

# यहाँ मैंने 6 बहुत ही सुंदर (Beautiful) फ़ोटोज़ के लिंक्स डाल दिए हैं
PROMO_IMAGES = [
    "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg",  # आपकी ओरिजिनल फोटो
    "https://files.catbox.moe/ddzvc0.jpg",                                  # आपकी दूसरी फोटो
    "https://telegra.ph/file/32b0c30953a9cd8ea265a.jpg",                    # Aesthetic Night Sky
    "https://telegra.ph/file/71f652b415b3c5825cfd3.jpg",                    # Music Vibes / Lo-Fi
    "https://telegra.ph/file/82633010b9fdb823ddf81.jpg",                    # Beautiful Setup
    "https://telegra.ph/file/8b1e42817ce8c94622c81.jpg"                     # Anime Aesthetic
]

@Client.on_message(filters.command(["promo", "promotion"]) & filters.user(OWNER_ID))
async def promo_message(client: Client, message: Message):
    
    # हर बार कमांड देने पर लिस्ट में से कोई एक अलग फोटो रैंडमली चुनी जाएगी
    random_img = random.choice(PROMO_IMAGES)
    
    # प्रमोशन का शानदार टेक्स्ट
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
    
    # Stacked Inline Buttons (एक के नीचे एक)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/RIYA_MUSIC_BOT_786")],
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{client.me.username}?startgroup=true")]
    ])
    
    try:
        # रैंडम चुनी गई फोटो के साथ मैसेज भेजना
        await message.reply_photo(
            photo=random_img,
            caption=promo_text,
            reply_markup=keyboard
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
  
