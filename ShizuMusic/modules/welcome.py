import os
import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@bot.on_message(filters.new_chat_members)
async def ai_welcome(client, message: Message):
    for member in message.new_chat_members:
        user_name = member.first_name
        group_name = message.chat.title
        user_mention = member.mention
        
        fallback_welcome = (
            f"✨ **Welcome to {group_name}**, {user_mention}! 🫧\n\n"
            f"Glad to have you here. Enjoy high-quality music and AI features!\n\n"
            f"⚡️ **Powered by MGB NOT FREE CODER**"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💌 CONTACT OWNER 💌", url="https://t.me/MGB_CODER")],
            [InlineKeyboardButton("⚡️ SUPPORT GROUP ⚡️", url="https://t.me/RIYA_MUSIC_BOT_786")]
        ])

        if not GEMINI_API_KEY:
            try:
                await message.reply_text(fallback_welcome, reply_markup=keyboard)
            except Exception:
                pass
            continue

        # Direct Gemini Pro API for Welcome Message
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        prompt = (
            f"Write a short, fun, and energetic welcome message in Hinglish for user '{user_name}' "
            f"who just joined the Telegram group '{group_name}'. Act as a cool music & AI bot named "
            f"'MGB NOT FREE CODER'. Use cute emojis. Max 3 lines."
        )
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
            result = response.json()
            if "candidates" in result:
                reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
                welcome_text = f"{reply_text}\n\n👤 **User:** {user_mention}\n⚡️ **Powered by MGB NOT FREE CODER**"
                await message.reply_text(welcome_text, reply_markup=keyboard)
            else:
                await message.reply_text(fallback_welcome, reply_markup=keyboard)
        except Exception:
            await message.reply_text(fallback_welcome, reply_markup=keyboard)
        
