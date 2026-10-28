import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🌐 यह एडवांस फंक्शन इंटरनेट से ऑटोमैटिक नई इमेज लाएगा
async def get_random_image():
    try:
        async with aiohttp.ClientSession() as session:
            # यहाँ हम Waifu Pics API का इस्तेमाल कर रहे हैं जो एकदम सेफ और बेहतरीन इमेजेस देता है
            async with session.get("https://api.waifu.pics/sfw/waifu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
    except Exception:
        pass
    # अगर API में कोई दिक्कत आई, तो यह बैकअप इमेज काम आएगी (एरर नहीं आएगा)
    return "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg"

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]) & filters.user(8853897167))
async def promo_message(client, message: Message):
    
    # बॉट तुरंत एक नई इमेज जनरेट कर रहा है
    random_img = await get_random_image()
    
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
        # बॉट फोटो के साथ प्रोमो भेजेगा
        await message.reply_photo(photo=random_img, caption=promo_text, reply_markup=keyboard)
    except Exception:
        # अगर कोई भी दिक्कत हुई तो बिना फोटो के सिर्फ टेक्स्ट भेज देगा
        await message.reply_text(text=promo_text, reply_markup=keyboard)
        
