import os
import google.generativeai as genai
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 🔥 404 Error Fix: gemini-1.5-flash की जगह gemini-pro कर दिया है
chat_model = genai.GenerativeModel("gemini-pro")

@bot.on_message(filters.command(["ask", "chat"], prefixes=["/", "!", "."]))
async def gemini_ask(client, message: Message):
    if not GEMINI_API_KEY:
        return await message.reply_text("❌ **Error:** Gemini API Key Render par set nahi hai!")
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/ask <सवाल>`")
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("⏳ **Gemini सोच रहा है...** 🫧")
    
    try:
        response = chat_model.generate_content(f"Answer concisely in Hinglish or English: {query}")
        await m.edit_text(f"🫧 **MGB AI:**\n\n{response.text}\n\n✨ _Powered by MGB NOT FREE CODER_")
    except Exception as e:
        await m.edit_text(f"❌ **Error:** `{e}`")

# 🔥 Image Error Fix: Superfast Direct API का इस्तेमाल (बिना क्रैश के)
@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def fast_draw(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/draw <prompt>`")

    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **Image बना रहा है...** 🫧")
    
    try:
        formatted_prompt = prompt.replace(" ", "%20")
        image_url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?width=1024&height=1024&nologo=true"
        
        await message.reply_photo(
            photo=image_url, 
            caption=f"🎨 **Prompt:** `{prompt}`\n\n✨ **Powered by MGB NOT FREE CODER**"
        )
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ **Image Error:** `{e}`")
        
