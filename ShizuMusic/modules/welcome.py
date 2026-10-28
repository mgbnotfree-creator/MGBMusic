import random
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🔥 10 प्रीमियम बैकअप इमेजेस (ताकि वेलकम भी कभी 1 फोटो पर न अटके!)
BACKUP_IMAGES = [
    "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg",
    "https://cdn.nekos.life/waifu/v01_020.png",
    "https://cdn.nekos.life/waifu/v01_025.png",
    "https://cdn.nekos.life/waifu/v01_030.png",
    "https://cdn.nekos.life/waifu/v01_035.png",
    "https://cdn.nekos.life/waifu/v01_040.png",
    "https://cdn.nekos.life/waifu/v01_045.png",
    "https://cdn.nekos.life/waifu/v01_050.png",
    "https://cdn.nekos.life/waifu/v01_060.png",
    "https://cdn.nekos.life/waifu/v01_070.png"
]

# 🌐 सुपरफास्ट API जो हर नए मेंबर के लिए नई फोटो लाएगा
async def get_random_image():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/waifu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
    except Exception:
        pass
    # अगर API फेल हुआ, तो बॉट 10 बैकअप इमेजेस में से कोई एक रैंडम फोटो उठा लेगा
    return random.choice(BACKUP_IMAGES)

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
            [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧nel", url="https://t.me/RIYA_MUSIC_BOT_786")],
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
            # अगर कोई भी दिक्कत हुई तो बिना फोटो के सिर्फ टेक्स्ट भेज देगा
            await message.reply_text(text=welcome_text, reply_markup=keyboard)
            
