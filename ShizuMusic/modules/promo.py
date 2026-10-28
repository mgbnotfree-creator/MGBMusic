import os
import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@bot.on_message(filters.command(["promo", "offers"], prefixes=["/", "!", "."]))
async def ai_promo(client, message: Message):
    m = await message.reply_text("⏳ **Generating premium MGB Promo...** ✨")
    
    # Aesthetic Buttons with Owner Branding
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💎 API PLANS 💎", url="https://t.me/MGB_CODER"),
            InlineKeyboardButton("💻 PAYMENT QR 💻", url="https://t.me/MGB_CODER")
        ],
        [
            InlineKeyboardButton("🫧 OWNER 🫧", url="https://t.me/MGB_CODER"),
            InlineKeyboardButton("✨ SOURCE ✨", url="https://t.me/MGB_CODER")
        ],
        [InlineKeyboardButton("💌 CONTACT OWNER 💌", url="https://t.me/MGB_CODER")],
        [InlineKeyboardButton("⚡️ SUPPORT GROUP ⚡️", url="https://t.me/RIYA_MUSIC_BOT_786")]
    ])

    if not GEMINI_API_KEY:
        return await m.edit_text(
            "💎 **MGB NOT FREE CODER SERVICES** 💎\n\n"
            "✨ **Available Services:**\n"
            " ├ High-Quality Telegram Music Bots\n"
            " ├ Advanced AI Chat & Image Bots\n"
            " ├ VPS & Render 24/7 Deployment\n"
            " └ Custom Python APIs & Database Setup\n\n"
            "**Owner ID:** `8853897167`\n\n"
            "💡 _After payment via QR, send the screenshot to our contact or support channel to activate your plan._", 
            reply_markup=keyboard
        )

    # Direct Gemini Pro API for Promo Generation
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    prompt = (
        "Write a highly engaging and aesthetic Telegram promotional message for 'MGB NOT FREE CODER'. "
        "Highlight services: Premium Music Bots, AI Bots, Render Deployment, and Custom APIs. "
        "Use aesthetic emojis (🫧, ✨, 💎, 💌), stylish formatting, and professional Hinglish. Keep it concise."
    )
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        result = response.json()
        if "candidates" in result:
            reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
            promo_caption = (
                f"{reply_text}\n\n"
                f"**Owner ID:** `8853897167`\n\n"
                f"💡 _After payment via QR, send the screenshot to our contact or support channel to activate your plan._"
            )
            await m.edit_text(text=promo_caption, reply_markup=keyboard)
        else:
            await m.edit_text(
                f"💎 **MGB NOT FREE CODER SERVICES** 💎\n\n"
                f"- High-Quality Music Bots\n- VPS & Render Deployment\n- Custom API Setup\n\n"
                f"**Owner ID:** `8853897167`", 
                reply_markup=keyboard
            )
    except Exception as e:
        await m.edit_text(f"❌ Promo Error: {e}")
        
