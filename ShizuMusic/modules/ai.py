import os
import google.generativeai as genai
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot

# Render से सुरक्षित तरीके से API Key उठाएगा
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

chat_model = genai.GenerativeModel("gemini-1.5-flash")

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

@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def gemini_draw(client, message: Message):
    if not GEMINI_API_KEY:
        return await message.reply_text("❌ **Error:** Gemini API Key set nahi hai!")
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/draw <prompt>`")

    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **Gemini AI image बना रहा है...** 🫧")

    try:
        imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
        result = imagen.generate_images(prompt=prompt, number_of_images=1, aspect_ratio="1:1")
        
        for image in result.images:
            await message.reply_photo(photo=image._image_bytes, caption=f"🎨 **Prompt:** `{prompt}`\n\n✨ **Powered by MGB NOT FREE CODER**")
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ **Image Error:** `{e}`")
        
