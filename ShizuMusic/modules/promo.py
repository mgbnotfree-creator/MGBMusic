import os
import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@bot.on_message(filters.command(["promo", "offers"], prefixes=["/", "!", "."]))
async def ai_promo(client, message: Message):
    m = await message.reply_text("⏳ **Generating premium MGB Promo...** ✨")
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 CONTACT OWNER 💌", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("⚡️ SUPPORT GROUP ⚡️", url="https://t.me/RIYA_MUSIC_BOT_786")]
    ])

    if not GEMINI_API_KEY:
        return await m.edit_text("💎 **MGB NOT FREE CODER SERVICES** 💎\n\n- High-Quality Music Bots\n- VPS & Render Deployment\n- Custom API Setup\n\n**Owner ID:** `8853897167`", reply_markup=keyboard)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    data = {
        "contents": [{"parts": [{"text": "Write a highly engaging aesthetic Telegram promo message for 'MGB NOT FREE CODER'. Services: Premium Music Bots, AI Bots, Render Deployment, Custom APIs. Use emojis (🫧, ✨, 💎). Professional Hinglish. Keep it short."}]}]
    }
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        result = response.json()
        if "candidates" in result:
            reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
            await m.edit_text(text=f"{reply_text}\n\n**Owner ID:** `8853897167`", reply_markup=keyboard)
        else:
            await m.edit_text(f"❌ **API Error:** {result.get('error', {}).get('message', 'Unknown Error')}")
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
        
