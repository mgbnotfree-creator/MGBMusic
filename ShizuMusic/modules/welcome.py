import os
import google.generativeai as genai
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    welcome_model = genai.GenerativeModel("gemini-1.5-flash")

@bot.on_message(filters.new_chat_members)
async def ai_welcome(client, message: Message):
    for member in message.new_chat_members:
        user_name = member.first_name
        group_name = message.chat.title
        
        if not GEMINI_API_KEY:
            return await message.reply_text(f"✨ Welcome to {group_name}, {user_name}! 🫧\n\n⚡️ Powered by MGB NOT FREE CODER")

        prompt = f"Write a short, funny welcome message in Hinglish for '{user_name}' who joined '{group_name}'. Do not use generic greetings, act as a cool bot named MGB NOT FREE CODER. Use emojis. Max 3 lines."
        
        try:
            response = welcome_model.generate_content(prompt)
            await message.reply_text(f"{response.text}\n\n⚡️ **Powered by MGB NOT FREE CODER**")
        except Exception:
            await message.reply_text(f"✨ Welcome to {group_name}, {user_name}! 🫧\n\n⚡️ Powered by MGB NOT FREE CODER")
            
