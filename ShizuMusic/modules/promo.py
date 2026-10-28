import os
import random
import requests
import base64
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🌟 HD AI प्रॉम्प्ट्स (Gemini Imagen 3 इन प्रॉम्प्ट्स से फोटो बनाएगा)
PROMPTS = [
    "beautiful aesthetic anime girl, 4k resolution, highly detailed, masterpiece",
    "cute anime girl in cyber neon city, 8k quality, glowing aesthetic",
    "gorgeous anime waifu, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "anime girl with sword, dark aesthetic, extremely detailed, hd"
]

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]) & filters.user(8853897167))
async def promo_message(client, message: Message):
    m = await message.reply_text("⏳ **Gemini AI HD Promo बना रहा है... थोड़ा इंतज़ार करें!** ✨")
    
    # 🔥 Client से बॉट का असली यूज़रनेम निकालना (Crash Fix)
    me = await client.get_me()
    bot_username = me.username
    
    # 🎯 Aero Music स्टाइल वाला कीबोर्ड
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
        "💌 ᴘᴏᴡᴇʀᴇᴅ ʙʏ : MGB NOT FREE CODER"
    )

    photo_to_send = None

    if GEMINI_API_KEY:
        # ==========================================
        # 1. GEMINI AI TEXT GENERATOR (Caption)
        # ==========================================
        try:
            text_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            text_prompt = (
                "Write a highly engaging and aesthetic Telegram promotional message for 'MGB NOT FREE CODER'. "
                "Highlight services: Premium Music Bots, AI Bots, Render Deployment, and Custom APIs. "
                "Use aesthetic emojis, stylish formatting, and professional Hinglish. Keep it concise. "
                "Do not use bold markdown for the main title."
            )
            text_data = {"contents": [{"parts": [{"text": text_prompt}]}]}
            text_res = requests.post(text_url, headers={'Content-Type': 'application/json'}, json=text_data).json()
            
            if "candidates" in text_res:
                generated_text = text_res["candidates"][0]["content"]["parts"][0]["text"]
                promo_text = f"{generated_text}\n\n💌 ᴘᴏᴡᴇʀᴇᴅ ʙʏ : MGB NOT FREE CODER"
        except Exception:
            pass # टेक्स्ट फेल हुआ तो डिफॉल्ट इस्तेमाल होगा

        # ==========================================
        # 2. GEMINI IMAGEN AI (Image Generator)
        # ==========================================
        try:
            img_prompt = random.choice(PROMPTS)
            img_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GEMINI_API_KEY}"
            img_data = {
                "instances": [{"prompt": img_prompt}],
                "parameters": {"sampleCount": 1}
            }
            img_res = requests.post(img_url, headers={'Content-Type': 'application/json'}, json=img_data).json()
            
            if "predictions" in img_res:
                # Gemini की इमेज Base64 फॉर्मेट में आती है, इसे डिकोड करके फोटो में बदलेंगे
                b64_img = img_res["predictions"][0]["bytesBase64Encoded"]
                photo_bytes = base64.b64decode(b64_img)
                photo_to_send = BytesIO(photo_bytes)
                photo_to_send.name = "mgb_promo.jpg"
        except Exception:
            pass # अगर इमेज फेल हुई तो सिर्फ टेक्स्ट जाएगा

    # ==========================================
    # 3. फाइनल मैसेज भेजना
    # ==========================================
    try:
        if photo_to_send:
            # Gemini ने फोटो बना ली है
            await message.reply_photo(photo=photo_to_send, caption=promo_text, reply_markup=keyboard)
        else:
            # बिना फोटो के सिर्फ टेक्स्ट भेजेगा
            await message.reply_text(text=promo_text, reply_markup=keyboard)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
        
