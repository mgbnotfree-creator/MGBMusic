import os
import requests
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShizuMusic import bot

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==========================================
# 🧠 GEMINI DIRECT API HELPER
# ==========================================
def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        return "❌ **Error:** Gemini API Key Render par set nahi hai!"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ **API Error:** {result.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"❌ **Error:** `{e}`"

# ==========================================
# 🤖 OLD FEATURE: AUTO CHATBOT (REPLY/MENTION)
# ==========================================
@bot.on_message(filters.text & ~filters.bot & ~filters.command(["ask", "draw", "speak", "aidj", "roast", "flirt", "shayari", "baba", "tod", "aimenu"]))
async def auto_chatbot(client, message: Message):
    bot_user = await client.get_me()
    
    # Check if bot is replied to OR mentioned
    is_replied = message.reply_to_message and message.reply_to_message.from_user.id == bot_user.id
    is_mentioned = message.text and f"@{bot_user.username}" in message.text
    
    if is_replied or is_mentioned:
        prompt = f"You are a cool, aesthetic Telegram bot named 'MGB NOT FREE CODER'. Reply in a friendly, short, and natural Hinglish way to this user's message: '{message.text}'"
        reply = get_gemini_response(prompt)
        await message.reply_text(f"🫧 {reply}")

# ==========================================
# 1. 🫧 AI CHAT COMMAND (/ask)
# ==========================================
@bot.on_message(filters.command(["ask", "chat"], prefixes=["/", "!", "."]))
async def gemini_ask(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/ask <सवाल>`")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("⏳ **Gemini सोच रहा है...** 🫧")
    reply = get_gemini_response(f"Answer concisely in Hinglish or English: {query}")
    await m.edit_text(f"🫧 **MGB AI:**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 2. 🎨 AI IMAGE GENERATOR (/draw)
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
        await message.reply_photo(photo=image_url, caption=f"🎨 **Prompt:** `{prompt}`\n\n✨ **Powered by MGB NOT FREE CODER**")
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ **Image Error:** `{e}`")

# ==========================================
# 3. 🎙️ AI VOICE NOTE (/speak)
# ==========================================
@bot.on_message(filters.command(["speak", "tts"], prefixes=["/", "!", "."]))
async def speak_text(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/speak <text>`")
    text = message.text.split(None, 1)[1]
    m = await message.reply_text("🎙️ **Voice record kar raha hu...** 🫧")
    try:
        tts = gTTS(text, lang='hi')
        tts.save("voice.mp3")
        await message.reply_voice("voice.mp3", caption="✨ **Powered by MGB NOT FREE CODER**")
        os.remove("voice.mp3")
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ **Voice Error:** `{e}`")

# ==========================================
# 4. 🎧 SMART AI DJ (/aidj)
# ==========================================
@bot.on_message(filters.command(["aidj", "dj"], prefixes=["/", "!", "."]))
async def smart_dj(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/aidj <mood/feeling>`\nExample: `/aidj romantic`")
    mood = message.text.split(None, 1)[1]
    m = await message.reply_text("🎧 **MGB DJ playlist bana raha hai...** 🎶")
    reply = get_gemini_response(f"Suggest 3 best Bollywood/Punjabi songs for '{mood}' mood. Just give names and singers with emojis. No long explanations.")
    await m.edit_text(f"🎧 **SMART DJ ({mood}):**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 5. 🔥 ROAST (/roast)
# ==========================================
@bot.on_message(filters.command(["roast"], prefixes=["/", "!", "."]))
async def ai_roast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("✨ **Usage:** Reply to any user's message with `/roast`")
    target_text = message.reply_to_message.text or "this user"
    m = await message.reply_text("🔥 **Roast mode ON...** 💀")
    reply = get_gemini_response(f"Roast this text hilariously in Hinglish, be funny but not extremely abusive: '{target_text}'")
    await m.edit_text(f"🔥 **ROASTED:**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 6. 💌 FLIRT & SHAYARI (/flirt or /shayari)
# ==========================================
@bot.on_message(filters.command(["flirt", "shayari"], prefixes=["/", "!", "."]))
async def ai_flirt(client, message: Message):
    m = await message.reply_text("💌 **Romantic line likh raha hu...** ✨")
    reply = get_gemini_response("Write a cute, romantic, and impressive 2-line Shayari or flirt line in Hinglish with aesthetic emojis.")
    await m.edit_text(f"💌 **SHAYARI:**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 7. 🔮 FUNNY BABA (/baba)
# ==========================================
@bot.on_message(filters.command(["baba", "future"], prefixes=["/", "!", "."]))
async def ai_baba(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Usage:** `/baba <question>`")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🔮 **Baba dhyaan laga rahe hain...** 🧘‍♂️")
    reply = get_gemini_response(f"Act as a funny Indian Baba predicting the future. Answer this question hilariously in Hinglish: '{query}'")
    await m.edit_text(f"🔮 **BABA JI SAYS:**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 8. 🃏 TRUTH OR DARE (/tod)
# ==========================================
@bot.on_message(filters.command(["tod"], prefixes=["/", "!", "."]))
async def ai_tod(client, message: Message):
    if len(message.command) < 2 or message.command[1].lower() not in ["truth", "dare"]:
        return await message.reply_text("✨ **Usage:** `/tod truth` OR `/tod dare`")
    choice = message.command[1].lower()
    m = await message.reply_text(f"🃏 **Generating a spicy {choice}...** ✨")
    reply = get_gemini_response(f"Give a fun, slightly tricky but safe '{choice}' question/task for a party game in Hinglish.")
    await m.edit_text(f"🃏 **YOUR {choice.upper()}:**\n\n{reply}\n\n✨ _Powered by MGB NOT FREE CODER_")

# ==========================================
# 9. 🫧 PREMIUM MENU (/aimenu)
# ==========================================
@bot.on_message(filters.command(["aimenu", "aihelp"], prefixes=["/", "!", "."]))
async def ai_menu(client, message: Message):
    menu_text = (
        "🫧 **MGB NOT FREE CODER - AI COMMANDS MENU** 🫧\n\n"
        "✨ **Available AI Features:**\n"
        " ├ `/ask <question>` - Gemini AI Chat\n"
        " ├ `/draw <prompt>` - HD AI Image Generator\n"
        " ├ `/speak <text>` - AI Voice Note (TTS)\n"
        " ├ `/aidj <mood>` - Smart AI Music DJ\n"
        " ├ `/roast` - Reply to message & roast\n"
        " ├ `/flirt` or `/shayari` - Romantic Shayaris\n"
        " ├ `/baba <question>` - Funny Future Predictor\n"
        " └ `/tod truth/dare` - Truth or Dare Game\n\n"
        "💌 _Note: You can also talk to me by replying to my messages!_"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🫧 ᴀɪ ᴄʜᴀᴛ 🫧", callback_data="ai_chat_info"),
            InlineKeyboardButton("✨ ᴀɪ ɪᴍᴀɢᴇs ✨", callback_data="ai_draw_info")
        ],
        [
            InlineKeyboardButton("🔮 sᴍᴀʀᴛ ᴅᴊ 🔮", callback_data="ai_dj_info"),
            InlineKeyboardButton("🎭 ʀᴏᴀsᴛ & ғᴜɴ 🎭", callback_data="ai_roast_info")
        ],
        [InlineKeyboardButton("💌 ᴏᴡɴᴇʀ ᴄᴏɴᴛᴀᴄᴛ 💌", url="https://t.me/MGB_CODER")]
    ])
    
    banner_url = "https://image.pollinations.ai/prompt/cyberpunk%20neon%20bot%20banner?width=1280&height=720&nologo=true"
    
    await message.reply_photo(
        photo=banner_url,
        caption=menu_text,
        reply_markup=keyboard
    )
    
