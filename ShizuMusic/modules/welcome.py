import os
import random
import aiohttp
import base64
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🌟 HD AI प्रॉम्प्ट्स (Pure Gemini Imagen 3 के लिए खुशमिजाज इमेजेस)
PROMPTS = [
    "beautiful aesthetic anime girl welcoming, 4k resolution, highly detailed",
    "cute anime girl waving hand smiling, cyber neon city, 8k quality, aesthetic",
    "gorgeous anime waifu smiling, sunset lighting, studio quality, hd",
    "aesthetic anime girl profile picture, lo-fi background, 4k",
    "beautiful anime girl with flowers, extremely detailed, hd"
]

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    # 🔥 Client से बॉट का असली यूज़रनेम और ID निकालना (Crash Fix)
    me = await client.get_me()
    bot_id = me.id
    bot_username = me.username

    for member in message.new_chat_members:
        # बॉट खुद का वेलकम नहीं करेगा
        if member.id == bot_id:
            continue
            
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
        welcome_text = (
            f"🎉 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏 🎉\n\n"
            f"✨ ʜᴇʏ {member.mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {message.chat.title}!\n\n"
            f"💎 ᴍᴇᴍʙᴇʀ ɪɴғᴏ:\n"
            f" ├ ɴᴀᴍᴇ: {member.first_name}\n"
            f" ├ ɪᴅ: {member.id}\n"
            f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
            f"💌 Powered by @MGB_NOT_FREE"
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
                        f"Write a short, aesthetic, and energetic welcome message for user '{member.first_name}' "
                        f"who joined '{message.chat.title}'. Keep it under 3 lines. Use emojis like 🎉, ✨, 💎. "
                        "Write in stylish Hinglish. Do not use bold markdown for the main title."
                    )
                    text_data = {"contents": [{"parts": [{"text": text_prompt}]}]}
                    
                    async with session.post(text_url, headers={'Content-Type': 'application/json'}, json=text_data) as t_res:
                        if t_res.status == 200:
                            t_json = await t_res.json()
                            if "candidates" in t_json:
                                generated_text = t_json["candidates"][0]["content"]["parts"][0]["text"]
                                welcome_text = (
                                    f"{generated_text}\n\n"
                                    f"💎 ᴍᴇᴍʙᴇʀ ɪɴғᴏ:\n"
                                    f" ├ ɴᴀᴍᴇ: {member.mention}\n"
                                    f" ├ ɪᴅ: {member.id}\n"
                                    f" └ ᴜsᴇʀɴᴀᴍᴇ: @{member.username if member.username else 'N/A'}\n\n"
                                    f"💌 Powered by @MGB_NOT_FREE"
                                )
                except Exception:
                    pass # फेल हुआ तो डिफॉल्ट टेक्स्ट यूज़ करेगा

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
                                photo_to_send.name = "mgb_welcome.jpg"
                        else:
                            img_err_msg = f"\n\n_(Note: AI Image Blocked - {i_res.status})_"
                except Exception:
                    pass # इमेज फेल हुई तो बिना फोटो के भेजेगा

        # ==========================================
        # 3. फाइनल वेलकम मैसेज भेजना
        # ==========================================
        try:
            if photo_to_send:
                # Gemini की बनाई हुई ताज़ा फोटो के साथ 
                await message.reply_photo(photo=photo_to_send, caption=welcome_text, reply_markup=keyboard)
            else:
                # बिना फोटो के (और अगर इमेज में एरर था तो बता देगा)
                await message.reply_text(text=welcome_text + img_err_msg, reply_markup=keyboard)
        except Exception:
            pass # वेलकम मैसेज में एरर प्रिंट नहीं करते ताकि ग्रुप में स्पैम ना हो
        
