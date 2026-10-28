import random
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# 🔥 10 प्रीमियम बैकअप इमेजेस (ताकि बॉट कभी भी 1 फोटो पर न अटके!)
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

# 🌐 सुपरफास्ट API जो Telegram सपोर्ट करता है
async def get_random_image():
    try:
        async with aiohttp.ClientSession() as session:
            # यहाँ हमने ज़्यादा सेफ Nekos.life API लगा दिया है
            async with session.get("https://nekos.life/api/v2/img/waifu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
    except Exception:
        pass
    # अगर API फेल हुआ, तो बॉट ऊपर दी गई 10 इमेजेस में से कोई एक रैंडम फोटो उठा लेगा
    return random.choice(BACKUP_IMAGES)

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
        await message.reply_photo(photo=random_img, caption=promo_text, reply_markup=keyboard)
    except Exception:
        await message.reply_text(text=promo_text, reply_markup=keyboard)
        
