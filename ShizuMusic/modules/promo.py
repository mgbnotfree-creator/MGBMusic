import os
import random
import aiohttp
import base64
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🌟 HD AI प्रॉम्प्ट्स (Pure Gemini Imagen 3 के लिए)
PROMPTS = [
    "beautiful aesthetic anime girl, 4k resolution, highly detailed, masterpiece",
    "cute anime girl in cyber neon city, 8k quality, glowing aesthetic",
    "gorgeous anime waifu, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "anime girl with sword, dark aesthetic, extremely detailed, hd"
]

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]) & filters.user(8853897167))
async def promo_message(client, message: Message):
    m = await message.reply_text("⏳ **Gemini AI HD Promo बना रहा है... Please wait!** 🕸️")
    
    # 🔥 Client से बॉट का असली यूज़रनेम निकालना (Crash Fix)
    me = await client.get_me()
    bot_username = me.username
    
    # 🎯 आपके नए एकदम खतरनाक Aesthetic बटन्स
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        [
            InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ", url="https://t.me/MGB_CODER"),
            InlineKeyboardButton("×̷̷͜×̷ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ", url="https://t.me/RIYA_MUSIC_BOT_786")
        ],
        [InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{bot_username}?startgroup=true")]
    ])
    
    # 📝 Default Fallback Text
    promo_text = (
        "🎉 𝐒𝐏𝐄𝐂𝐈𝐀𝐋 𝐏𝐑𝐎𝐌𝐎𝐓𝐈𝐎𝐍 🎉\n\n"
        "✨ MGB NOT FREE CODER ᴋɪ ᴛᴀʀᴀғ sᴇ ʙᴇsᴛ ᴏғғᴇʀs!\n\n"
        "🔥 ᴀɢᴀʀ ᴀᴀᴘᴋᴏ ᴀᴘɴᴀ ᴋʜᴜᴅ ᴋᴀ ᴍᴜsɪᴄ ʙᴏᴛ, ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʏᴀ "
        "ᴋɪsɪ ʙʜɪ ᴛᴀʀᴀʜ ᴋᴀ ᴘʏᴛʜᴏɴ ᴘʀᴏᴊᴇᴄᴛ ʙᴀɴᴡᴀɴᴀ ʜᴀɪ, ᴛᴏʜ ᴀᴀᴊ ʜɪ ᴄᴏɴᴛᴀᴄᴛ ᴋᴀʀᴇɪɴ!\n\n"
        "💎 ᴏᴜʀ sᴇʀᴠɪᴄᴇs:\n"
        " ├ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ ʙᴏᴛs\n"
        " ├ ᴠᴘs & ʀᴇɴᴅᴇʀ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ\n"
        " └ ᴄᴜsᴛᴏᴍ ᴀᴘɪ & ᴅᴀᴛᴀʙᴀsᴇ sᴇᴛᴜᴘ\n\n"
        "💌 Powered by @MGB_NOT_FREE"
    )

    photo_to_send = None
    img_err_msg = ""

    if GEMINI_API_KEY:
        async with aiohttp.ClientSession() as session:
            # ==========================================
            # 1. SUPERFAST TEXT GENERATOR (gemini-1.5-flash)
            # ==========================================
            try:
                text_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                text_prompt = (
                    "Write a highly engaging and aesthetic Telegram promotional message for 'MGB NOT FREE CODER'. "
                    "Highlight services: Premium Music Bots, AI Bots, Render Deployment, and Custom APIs. "
                    "Use aesthetic emojis, stylish formatting, and professional Hinglish. Keep it concise. "
                    "Do not use bold markdown for the main title."
                )
                text_data = {"contents": [{"parts": [{"text": text_prompt}]}]}
                
                async with session.post(text_url, headers={'Content-Type': 'application/json'}, json=text_data) as t_res:
                    if t_res.status == 200:
                        t_json = await t_res.json()
                        if "candidates" in t_json:
                            generated_text = t_json["candidates"][0]["content"]["parts"][0]["text"]
                            promo_text = f"{generated_text}\n\n💌 Powered by @MGB_NOT_FREE"
            except Exception:
                pass # अगर टेक्स्ट फेल हुआ तो पुराना Fallback यूज़ करेगा

            # ==========================================
            # 2. IMAGE GENERATOR (Imagen 3)
            # ==========================================
            try:
                img_prompt = random.choice(PROMPTS)
                img_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GEMINI_API_KEY}"
                img_data = {
                    "instances": [{"prompt": img_prompt}],
                    "parameters": {"sampleCount": 1}
                }
                
                async with session.post(img_url, headers={'Content-Type': 'application/json'}, json=img_data) as i_res:
                    if i_res.status == 200:
                        i_json = await i_res.json()
                        if "predictions" in i_json:
                            b64_img = i_json["predictions"][0]["bytesBase64Encoded"]
                            photo_bytes = base64.b64decode(b64_img)
                            photo_to_send = BytesIO(photo_bytes)
                            photo_to_send.name = "mgb_promo.jpg"
                    else:
                        img_err_msg = f"\n\n_(Note: Image Generation Blocked by Google API - {i_res.status})_"
            except Exception:
                pass

    # ==========================================
    # 3. फाइनल मैसेज भेजना
    # ==========================================
    try:
        if photo_to_send:
            # Gemini ने फोटो बना ली है
            await message.reply_photo(photo=photo_to_send, caption=promo_text, reply_markup=keyboard)
        else:
            # बिना फोटो के सिर्फ टेक्स्ट भेजेगा (और अगर इमेज में एरर था तो बता देगा)
            await message.reply_text(text=promo_text + img_err_msg, reply_markup=keyboard)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
    
