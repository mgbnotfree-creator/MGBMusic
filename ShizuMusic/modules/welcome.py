import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🌐 यह फंक्शन इंटरनेट से ऑटोमैटिक नई इमेज लाएगा (Welcome के लिए)
async def get_random_image():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/waifu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
    except Exception:
        pass
    # अगर इंटरनेट डाउन हुआ, तो बैकअप के लिए आपकी पहली इमेज जाएगी
    return "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg"

# जब भी कोई नया मेंबर ग्रुप में आएगा
@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    for member in message.new_chat_members:
        
        # बॉट खुद का वेलकम नहीं करेगा
        if member.id == bot.me.id:
            continue
            
        # बॉट तुरंत एक नई इमेज जनरेट कर रहा है
        random_img = await get_random_image()
        
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
            # बॉट नई फोटो के साथ वेलकम मैसेज भेजेगा
            await message.reply_photo(
                photo=random_img,
                caption=welcome_text,
                reply_markup=keyboard
            )
        except Exception:
            # अगर कोई भी दिक्कत हुई तो बिना फोटो के सिर्फ टेक्स्ट भेज देगा (एरर नहीं आएगा)
            await message.reply_text(text=welcome_text, reply_markup=keyboard)
            
