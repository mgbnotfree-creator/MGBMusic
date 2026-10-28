import os
import requests
from pyrogram import filters
from pyrogram.types import Message
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==========================================
# 1. 🫧 AI CHAT (/ask) - Direct API
# ==========================================
@bot.on_message(filters.command(["ask", "chat"], prefixes=["/", "!", "."]))
async def gemini_ask(client, message: Message):
    if not GEMINI_API_KEY:
        return await message.reply_text("❌ Gemini API Key missing in Render!")
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/ask <सवाल>`")
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("⏳ **Gemini सोच रहा है...** 🫧")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": f"Answer concisely in Hinglish or English: {query}"}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if "candidates" in result:
            reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
            await m.edit_text(f"🫧 **MGB AI:**\n\n{reply_text}\n\n✨ _Powered by MGB NOT FREE CODER_")
        else:
            error_msg = result.get('error', {}).get('message', 'Unknown Error')
            await m.edit_text(f"❌ **API Error:** {error_msg}")
    except Exception as e:
        await m.edit_text(f"❌ **Error:** `{e}`")

# ==========================================
# 2. 🎨 FAST IMAGE GENERATOR (/draw) 
# ==========================================
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
    
