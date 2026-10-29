import random
import urllib.parse
import aiohttp
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# ==========================================
# 🧠 1. SUPERFAST TEXT AI (Free ChatGPT API)
# ==========================================
async def fetch_ai_text(prompt, system_prompt=""):
    encoded_prompt = urllib.parse.quote(prompt)
    encoded_system = urllib.parse.quote(system_prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}?system={encoded_system}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                return "❌ **AI Server busy hai, thodi der baad try karein!**"
    except Exception as e:
        return f"❌ **Error:** `{e}`"

# ==========================================
# 🎨 2. PREMIUM HD IMAGE API (Lexica AI)
# ==========================================
async def fetch_hd_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://lexica.art/api/v1/search?q={encoded_prompt}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and "images" in data and len(data["images"]) > 0:
                        return random.choice(data["images"][:3])["src"], None
                return None, "❌ Image server busy hai!"
    except Exception as e:
        return None, f"❌ Image Error: {e}"
    return None, "Unknown Image Error"

# ==========================================
# 1. 🤖 AI Chatbot
# ==========================================
@bot.on_message(filters.command(["ask", "ai", "chat"], prefixes=["/", "!", "."]))
async def ai_chat(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ Boss, koi sawal pucho!\nExample: `/ask Who is Elon Musk?`")
    
    query = message.text.split(None, 1)[1]
    system = "You are a smart AI assistant created by MGB NOT FREE CODER. Answer politely and concisely in Hinglish."
    
    m = await message.reply_text("🔄 **MGB AI soch raha hai...** ✦")
    answer = await fetch_ai_text(query, system)
    await m.edit_text(f"𓆩🤖𓆪 **MGB AI:**\n\n{answer}\n\n💌 Powered by @MGB_NOT_FREE")

# ==========================================
# 2. 🎨 AI Image Creator (/draw)
# ==========================================
@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def ai_draw(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ Boss, kya banwana hai?\nExample: `/draw a beautiful anime girl in cyber city`")
    
    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **MGB AI Premium HD photo bana raha hai... Please wait!** 🕸️")
    
    img_url, err_msg = await fetch_hd_image(prompt)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    if img_url:
        try:
            await message.reply_photo(
                photo=img_url, 
                caption=f"🎨 **Prompt:** {prompt}\n\n💌 Powered by @MGB_NOT_FREE",
                reply_markup=keyboard
            )
            await m.delete()
        except Exception:
            await m.edit_text("❌ Photo Telegram par bhejne mein dikkat aayi!")
    else:
        await m.edit_text(err_msg)

# ==========================================
# 3. 🔊 AI Voice Note (Text-to-Speech)
# ==========================================
@bot.on_message(filters.command(["speak", "tts"], prefixes=["/", "!", "."]))
async def ai_speak(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ Boss, kya bolwana hai?\nExample: `/speak MGB Not Free Coder is the best!`")
    
    text = message.text.split(None, 1)[1]
    m = await message.reply_text("🗣️ **MGB AI bol raha hai...** ✦")
    
    try:
        tts = gTTS(text=text, lang='hi')
        file_name = f"voice_{message.from_user.id}.mp3"
        tts.save(file_name)
        
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        
        await message.reply_voice(
            voice=file_name, 
            caption="💌 Powered by @MGB_NOT_FREE",
            reply_markup=keyboard
        )
        await m.delete()
        
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as e:
        await m.edit_text(f"❌ Voice banane mein error aayi: {e}")

# ==========================================
# 4. 🎵 AI Smart DJ
# ==========================================
@bot.on_message(filters.command(["aidj", "mood"], prefixes=["/", "!", "."]))
async def ai_dj(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ Boss, mood kaisa hai?\nExample: `/aidj romantic` or `/aidj sad`")
    
    mood = message.text.split(None, 1)[1]
    m = await message.reply_text(f"🎵 **MGB AI aapke '{mood}' mood ke liye best gaane dhoondh raha hai...** 🍷")
    
    system = "You are an expert Music DJ. Suggest exactly 5 best Bollywood/Punjabi songs for the given mood. Format as a numbered list with Song Name and Artist. Don't add extra text."
    songs = await fetch_ai_text(f"Mood: {mood}", system)
    
    dj_text = f"🎧 **MGB AI SMART DJ** 🎧\n\n✦ **Aapka Mood:** {mood}\n\n{songs}\n\n💌 _Gaana sunne ke liye type karein /play <song name>_"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    await m.edit_text(dj_text, reply_markup=keyboard)

# ==========================================
# 5. 😈 AI Roast Master
# ==========================================
@bot.on_message(filters.command(["roast", "beizzati"], prefixes=["/", "!", "."]))
async def ai_roast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("✦ **Boss, kisi ke message ka reply karke /roast likho!** Tabhi toh asli maza aayega! ☠️")
    
    target_text = message.reply_to_message.text or "kuch ajeeb sa bheja hai"
    target_name = message.reply_to_message.from_user.first_name if message.reply_to_message.from_user else "is bande"
    
    m = await message.reply_text("☠️ **MGB AI Roast load kar raha hai... 🔥**")
    
    system = "You are a savage, funny, and brutal roast master created by MGB NOT FREE CODER. Roast the person in a very funny Hinglish style. Keep it short, savage, and entertaining. Don't use extreme swear words."
    roast_text = await fetch_ai_text(f"Roast this person named {target_name} who said: '{target_text}'", system)
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    await m.edit_text(f"☠️ **ROASTED BY MGB AI** ☠️\n\n👤 **Target:** {target_name}\n🔥 **Roast:** {roast_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

# ==========================================
# 6. 💔 AI Shayari & Flirt Master 
# ==========================================
@bot.on_message(filters.command(["shayari", "flirt"], prefixes=["/", "!", "."]))
async def ai_shayari(client, message: Message):
    prompt = ""
    target_name = ""

    if message.reply_to_message:
        target_name = message.reply_to_message.from_user.first_name if message.reply_to_message.from_user else "is cute bande/bandi"
        prompt = f"Write a very impressive, romantic and smooth flirt line in Hinglish for {target_name}."
    elif len(message.command) > 1:
        topic = message.text.split(None, 1)[1]
        prompt = f"Write a 4-line killer Hindi/Hinglish shayari about: {topic}."
    else:
        prompt = "Write a random 4-line attitude or love shayari in Hinglish."
    
    system = "You are a romantic, stylish, and smooth Shayar and Flirt master created by MGB NOT FREE CODER. Write short, impressive Hinglish poetry or flirt lines. Use emojis. Make it cool and savage."
    m = await message.reply_text("🍷 **MGB AI aapke liye kuch special likh raha hai... ✨**")
    
    result_text = await fetch_ai_text(prompt, system)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    header = f"🍷 **FLIRT MACHINE** 🍷\n👤 **Target:** {target_name}\n\n" if target_name else "🍷 **MGB AI SHAYARI** 🍷\n\n"
    
    await m.edit_text(f"{header}{result_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

# ==========================================
# 7. 🔮 AI Baba / Astrologer 
# ==========================================
@bot.on_message(filters.command(["baba", "future"], prefixes=["/", "!", "."]))
async def ai_baba(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ Bacha, pehle apna sawal toh pucho!\nExample: `/baba meri shadi kab hogi?`")
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("📿 **MGB Baba dhyaan laga rahe hain... 🧘‍♂️**")
    
    system = "You are a funny, savage, and dramatic Indian Baba/Astrologer created by MGB NOT FREE CODER. Answer the user's question about their future in Hinglish. Make it very funny, roasting, and humorous. Use words like 'Vats', 'Bacha', 'Tathastu'."
    answer = await fetch_ai_text(query, system)
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    await m.edit_text(f"𓆩♛𓆪 **MGB BABA BHAWISHYAWANI** 𓆩♛𓆪\n\n🗣️ **Bhakht ka Sawal:** {query}\n\n🧘‍♂️ **Baba ka Jawab:** {answer}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

# ==========================================
# 8. 🎭 AI Meme Generator 
# ==========================================
@bot.on_message(filters.command(["meme", "joke"], prefixes=["/", "!", "."]))
async def ai_meme(client, message: Message):
    topic = message.text.split(None, 1)[1] if len(message.command) > 1 else "random dank programming or life"
    prompt = f"Make a very funny meme text or joke about: {topic}"
    
    m = await message.reply_text("🎭 **MGB AI dank meme dhoondh raha hai... 😂**")
    
    system = "You are a dank meme generator created by MGB NOT FREE CODER. Write a very funny, short, and savage meme text or joke in Hinglish. Use relevant emojis."
    meme_text = await fetch_ai_text(prompt, system)
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    await m.edit_text(f"🎭 **MGB MEME ZONE** 🎭\n\n{meme_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

# ==========================================
# 9. 🎲 AI Truth or Dare (TOD)
# ==========================================
@bot.on_message(filters.command(["tod", "truthordare"], prefixes=["/", "!", "."]))
async def ai_tod(client, message: Message):
    if len(message.command) < 2 or message.command[1].lower() not in ["truth", "dare"]:
        return await message.reply_text("✦ Boss, sahi se batao!\nExample: `/tod truth` ya `/tod dare`")
    
    choice = message.command[1].lower()
    prompt = f"Give me a {choice} question/task"
    
    m = await message.reply_text(f"🃏 **MGB AI aapke liye ek khatarnak {choice} nikal raha hai... 😈**")
    
    system = f"You are a fun Truth or Dare game master created by MGB NOT FREE CODER. The user chose {choice}. Give a funny, creative, and slightly embarrassing but safe {choice} in Hinglish. Keep it short. Use emojis."
    tod_text = await fetch_ai_text(prompt, system)
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    await m.edit_text(f"🃏 **MGB TRUTH OR DARE** 🃏\n\n🎯 **Choice:** {choice.upper()}\n😈 **Task:** {tod_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)

# ==========================================
# 10. 𓆩♛𓆪 AI Interactive Menu
# ==========================================
@bot.on_message(filters.command(["aimenu", "aihelp"], prefixes=["/", "!", "."]))
async def ai_menu(client, message: Message):
    menu_text = (
        "𓆩♛𓆪 **MGB NOT FREE CODER - AI MENU** 𓆩♛𓆪\n\n"
        "✦ **Available AI Features:**\n"
        " ├ `/ask` - Smart AI Chat\n"
        " ├ `/draw` - Premium HD Images\n"
        " ├ `/speak` - AI Voice Note\n"
        " ├ `/aidj` - Smart AI Music DJ\n"
        " ├ `/roast` - Savage Roast\n"
        " ├ `/flirt` / `/shayari` - Love Shayari\n"
        " ├ `/baba` - Future Predictor\n"
        " ├ `/meme` - Dank AI Memes\n"
        " └ `/tod` - Truth or Dare\n\n"
        "×̷̷͜×̷ *Select any option below!*"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✦ ᴀɪ ᴄʜᴀᴛ", callback_data="ai_chat_info"),
            InlineKeyboardButton("🕸️ ᴀɪ ɪᴍᴀɢᴇs", callback_data="ai_draw_info")
        ],
        [
            InlineKeyboardButton("🍷 sᴍᴀʀᴛ ᴅᴊ", callback_data="ai_dj_info"),
            InlineKeyboardButton("☠️ ʀᴏᴀsᴛ & ғᴜɴ", callback_data="ai_roast_info")
        ],
        [InlineKeyboardButton("🦅 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 🦅", url="https://t.me/MGB_CODER")]
    ])
    
    await message.reply_text(menu_text, reply_markup=keyboard)
    
