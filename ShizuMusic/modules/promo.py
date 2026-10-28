import os
import google.generativeai as genai
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    promo_model = genai.GenerativeModel("gemini-1.5-flash")

@bot.on_message(filters.command(["promo", "offers"], prefixes=["/", "!", "."]))
async def ai_promo(client, message: Message):
    m = await message.reply_text("⏳ **Generating premium MGB Promo...** ✨")
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 CONTACT OWNER 💌", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("⚡️ SUPPORT GROUP ⚡️", url="https://t.me/RIYA_MUSIC_BOT_786")]
    ])

    if not GEMINI_API_KEY:
        return await m.edit_text("💎 **MGB NOT FREE CODER SERVICES** 💎\n\n- High-Quality Music Bots\n- VPS & Render Deployment\n- Custom API Setup\n\n**Owner ID:** `8853897167`", reply_markup=keyboard)

    prompt = "Write a highly engaging aesthetic Telegram promo message for 'MGB NOT FREE CODER'. Services: Premium Music Bots, AI Bots, Render Deployment, Custom APIs. Use emojis (🫧, ✨, 💎). Professional Hinglish. Keep it short."
    
    try:
        response = promo_model.generate_content(prompt)
        await m.edit_text(text=f"{response.text}\n\n**Owner ID:** `8853897167`", reply_markup=keyboard)
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
        
