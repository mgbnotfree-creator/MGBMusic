import os
import shutil
import random
import urllib.parse
import aiohttp
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from ShizuMusic import bot

# ==========================================
# 🧠 1. ADVANCED ACCURATE TEXT AI
# ==========================================
async def fetch_advanced_ai_text(prompt, system_prompt=""):
    enhanced_system = (
        "You are an elite, highly intelligent, and strictly factual AI assistant created by MGB NOT FREE CODER. "
        "Provide accurate, deep, well-researched, and structured answers in stylish Hinglish. "
        "Never give false or vague information. Be precise and professional."
    )
    if system_prompt:
        enhanced_system += f" {system_prompt}"
        
    encoded_prompt = urllib.parse.quote(prompt)
    encoded_system = urllib.parse.quote(enhanced_system)
    url = f"https://text.pollinations.ai/{encoded_prompt}?system={encoded_system}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                return "❌ **AI Server busy hai, kripya thodi der baad try karein!**"
    except Exception as e:
        return f"❌ **Error:** `{e}`"

# ==========================================
# 🎨 2. ADVANCED LEXICA & POLLINATIONS 4K IMAGE API
# ==========================================
async def generate_advanced_ai_image(prompt):
    encoded_prompt = urllib.parse.quote(f"{prompt} highly detailed 4k resolution masterpiece aesthetic")
    lexica_url = f"https://lexica.art/api/v1/search?q={encoded_prompt}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(lexica_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and "images" in data and len(data["images"]) > 0:
                        return random.choice(data["images"][:5])["src"]
    except Exception:
        pass
    
    refined_prompt = f"masterpiece, ultra detailed 4k, professional digital art, {prompt}, flawless lighting, high definition"
    encoded_pollination = urllib.parse.quote(refined_prompt)
    seed = random.randint(1000, 999999)
    return f"https://image.pollinations.ai/prompt/{encoded_pollination}?width=1280&height=1280&seed={seed}&nologo=true&enhance=true"

# ==========================================
# 1. 🤖 Advanced AI Chatbot (/ask)
# ==========================================
@bot.on_message(filters.command(["ask", "ai", "chat"], prefixes=["/", "!", "."]))
async def ai_chat(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_advanced_ai_image("advanced futuristic intelligent cyberpunk AI 4k wallpaper")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ **Boss, koi advanced sawal pucho!**\nExample: `/ask Black hole kya hota hai?`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🧠 **MGB Advanced AI research kar raha hai...** ✦")
    
    answer = await fetch_advanced_ai_text(query)
    top_img = await generate_advanced_ai_image(f"conceptual digital art representing {query}")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=f"𓆩🤖𓆪 **MGB ADVANCED AI ZONE:**\n\n💬 **Sawal:** `{query}`\n\n{answer}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 2. 🎨 AI Image Creator (/draw)
# ==========================================
@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def ai_draw(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_advanced_ai_image("stunning cyberpunk city neon aesthetic anime 4k")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ **Boss, kya banwana hai?**\nExample: `/draw a beautiful anime girl in a neon cyber city`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **MGB Advanced AI 4K Masterpiece render kar raha hai... Please wait!** 🕸️")
    
    img_url = await generate_advanced_ai_image(prompt)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    try:
        await message.reply_photo(photo=img_url, caption=f"🎨 **Generated Prompt:** `{prompt}`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
        await m.delete()
    except Exception as e:
        await message.reply_text(f"❌ Photo bhejne mein error aayi: {e}")
        await m.delete()

# ==========================================
# 3. 🔊 AI Voice Note (Text-to-Speech + Storage Trick)
# ==========================================
@bot.on_message(filters.command(["speak", "tts"], prefixes=["/", "!", "."]))
async def ai_speak(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_advanced_ai_image("music sound waves aesthetic neon anime")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ **Boss, kya bolwana hai?**\nExample: `/speak MGB Coder is genius!`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    text = message.text.split(None, 1)[1]
    m = await message.reply_text("🗣️ **MGB AI voice generate kar raha hai...** ✦")
    file_name = f"voice_{message.from_user.id}.mp3"
    
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save(file_name)
        
        top_img = await generate_advanced_ai_image("singing anime girl cute headphones 4k")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        
        await message.reply_photo(photo=top_img, caption=f"🗣️ **AI Voice Note:** `{text}`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
        await message.reply_voice(voice=file_name)
        await m.delete()
    except Exception as e:
        await message.reply_text(f"❌ Voice banane mein error aayi: {e}")
        await m.delete()
    finally:
        # 🌟 STORAGE FULL TRICK 🌟
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except:
                pass

# ==========================================
# 4. 🎵 AI Smart DJ
# ==========================================
@bot.on_message(filters.command(["aidj", "mood"], prefixes=["/", "!", "."]))
async def ai_dj(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_advanced_ai_image("dj party neon music concert anime 4k")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ **Boss, mood kaisa hai?**\nExample: `/aidj romantic` or `/aidj sad`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    mood = message.text.split(None, 1)[1]
    m = await message.reply_text(f"🎵 **MGB AI aapke '{mood}' mood ke liye best gaane analyze kar raha hai...** 🍷")
    
    system = "Suggest exactly 5 accurate and popular Bollywood/Punjabi songs for the given mood as a clean numbered list."
    songs = await fetch_advanced_ai_text(f"Mood: {mood}", system)
    
    dj_text = f"🎧 **MGB ADVANCED AI DJ** 🎧\n\n✦ **Aapka Mood:** {mood}\n\n{songs}\n\n💌 _Gaana sunne ke liye type karein /play <song name>_\n\n💌 Powered by @MGB_NOT_FREE"
    top_img = await generate_advanced_ai_image(f"{mood} music mood aesthetic anime girl")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=dj_text, reply_markup=keyboard)
    await m.delete()

# ==========================================
# 5. 😈 AI Roast Master
# ==========================================
@bot.on_message(filters.command(["roast", "beizzati"], prefixes=["/", "!", "."]))
async def ai_roast(client, message: Message):
    if not message.reply_to_message:
        top_img = await generate_advanced_ai_image("savage angry anime character fire background")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ **Boss, kisi ke message ka reply karke /roast likho!** Tabhi toh asli maza aayega! ☠️\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    target_text = message.reply_to_message.text or "kuch ajeeb sa bheja hai"
    target_name = message.reply_to_message.from_user.first_name if message.reply_to_message.from_user else "is bande"
    m = await message.reply_text("☠️ **MGB Advanced Roast load ho raha hai... 🔥**")
    
    system = "Roast the person in a very funny, clever, and savage Hinglish style without being overly toxic."
    roast_text = await fetch_advanced_ai_text(f"Roast this person named {target_name} who said: '{target_text}'", system)
    
    top_img = await generate_advanced_ai_image("funny savage angry anime meme face")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=f"☠️ **ADVANCED ROASTED BY MGB AI** ☠️\n\n👤 **Target:** {target_name}\n🔥 **Roast:** {roast_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 6. 💔 AI Shayari & Flirt Master 
# ==========================================
@bot.on_message(filters.command(["shayari", "flirt"], prefixes=["/", "!", "."]))
async def ai_shayari(client, message: Message):
    prompt, target_name = "", ""
    if message.reply_to_message:
        target_name = message.reply_to_message.from_user.first_name if message.reply_to_message.from_user else "is cute bande/bandi"
        prompt = f"Write a very impressive, intelligent, and smooth flirt line in Hinglish for {target_name}."
    elif len(message.command) > 1:
        topic = message.text.split(None, 1)[1]
        prompt = f"Write a deep and poetic 4-line Hindi/Hinglish shayari about: {topic}."
    else:
        prompt = "Write a soulful 4-line love shayari in Hinglish."
    
    system = "Write creative, heart-touching, and stylish Hinglish poetry with nice emojis."
    m = await message.reply_text("🍷 **MGB Advanced AI shayari craft kar raha hai... ✨**")
    
    result_text = await fetch_advanced_ai_text(prompt, system)
    top_img = await generate_advanced_ai_image("romantic sunset aesthetic anime couple 4k")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    header = f"🍷 **ADVANCED FLIRT MACHINE** 🍷\n👤 **Target:** {target_name}\n\n" if target_name else "🍷 **MGB AI SHAYARI** 🍷\n\n"
    
    await message.reply_photo(photo=top_img, caption=f"{header}{result_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 7. 🔮 AI Baba / Astrologer 
# ==========================================
@bot.on_message(filters.command(["baba", "future"], prefixes=["/", "!", "."]))
async def ai_baba(client, message: Message):
    if len(message.command) < 2:
        top_img = await generate_advanced_ai_image("mystic magic wizard glowing crystal ball 4k")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ Bacha, pehle apna sawal toh pucho!\nExample: `/baba meri shadi kab hogi?`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("📿 **MGB Baba divya drishti laga rahe hain... 🧘‍♂️**")
    
    system = "Answer as a witty, dramatic, and humorous Indian Baba in Hinglish using words like 'Vats', 'Bacha', 'Tathastu'."
    answer = await fetch_advanced_ai_text(query, system)
    
    top_img = await generate_advanced_ai_image("fortune teller mystic prophecy glowing magic")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=f"𓆩♛𓆪 **MGB ADVANCED BABA BHAWISHYAWANI** 𓆩♛𓆪\n\n🗣️ **Bhakht ka Sawal:** {query}\n\n🧘‍♂️ **Baba ka Jawab:** {answer}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 8. 🎭 AI Meme Generator (Funny Image + Text)
# ==========================================
@bot.on_message(filters.command(["meme", "joke"], prefixes=["/", "!", "."]))
async def ai_meme(client, message: Message):
    topic = message.text.split(None, 1)[1] if len(message.command) > 1 else "coding and developer life"
    m = await message.reply_text("🎭 **MGB Advanced AI dank meme generate kar raha hai... 😂**")
    
    system = "Write a clever, highly relatable, and funny tech/life meme text in Hinglish with emojis."
    meme_text = await fetch_advanced_ai_text(f"Make a funny meme text about: {topic}", system)
    
    top_img = await generate_advanced_ai_image(f"funny hilarious dank meme cartoon reaction about {topic}")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=f"🎭 **MGB ADVANCED MEME ZONE** 🎭\n\n{meme_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 9. 🎲 AI Truth or Dare (TOD)
# ==========================================
@bot.on_message(filters.command(["tod", "truthordare"], prefixes=["/", "!", "."]))
async def ai_tod(client, message: Message):
    if len(message.command) < 2 or message.command[1].lower() not in ["truth", "dare"]:
        top_img = await generate_advanced_ai_image("gaming neon aesthetic challenge mystery")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        return await message.reply_photo(photo=top_img, caption="✦ Boss, sahi se batao!\nExample: `/tod truth` ya `/tod dare`\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    
    choice = message.command[1].lower()
    m = await message.reply_text(f"🃏 **MGB AI ek mazedaar {choice} task nikal raha hai... 😈**")
    
    system = f"Give a creative, entertaining, and safe {choice} challenge in Hinglish."
    tod_text = await fetch_advanced_ai_text(f"Give a creative {choice} challenge.", system)
    
    top_img = await generate_advanced_ai_image(f"mystery game challenge {choice} anime aesthetic")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    await message.reply_photo(photo=top_img, caption=f"🃏 **MGB ADVANCED TRUTH OR DARE** 🃏\n\n🎯 **Choice:** {choice.upper()}\n😈 **Task:** {tod_text}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=keyboard)
    await m.delete()

# ==========================================
# 10. 𓆩♛𓆪 AI Interactive Menu
# ==========================================
@bot.on_message(filters.command(["aimenu", "aihelp"], prefixes=["/", "!", "."]))
async def ai_menu(client, message: Message):
    menu_text = (
        "𓆩♛𓆪 **MGB ADVANCED AI - CONTROL PANEL** 𓆩♛𓆪\n\n"
        "✦ **Available Advanced Features:**\n"
        " ├ `/ask` - Smart Accurate AI Chat\n"
        " ├ `/draw` - Real-time 4K Image Generator\n"
        " ├ `/speak` - AI Voice Studio\n"
        " ├ `/aidj` - Smart AI Music DJ\n"
        " ├ `/roast` - Savage Roast Master\n"
        " ├ `/flirt` / `/shayari` - Soulful Shayari\n"
        " ├ `/baba` - Future Predictor\n"
        " ├ `/meme` - Funny Meme & Image\n"
        " └ `/tod` - Truth or Dare\n\n"
        "×̷̷͜×̷ *Select any option below!*\n\n💌 Powered by @MGB_NOT_FREE"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ ᴀɪ ᴄʜᴀᴛ", callback_data="ai_chat_info"), InlineKeyboardButton("🕸️ ᴀɪ ɪᴍᴀɢᴇs", callback_data="ai_draw_info")],
        [InlineKeyboardButton("🍷 sᴍᴀʀᴛ ᴅᴊ", callback_data="ai_dj_info"), InlineKeyboardButton("☠️ ʀᴏᴀsᴛ & ғᴜɴ", callback_data="ai_roast_info")],
        [InlineKeyboardButton("🦅 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 🦅", url="https://t.me/MGB_CODER")]
    ])
    top_img = await generate_advanced_ai_image("cyberpunk luxury AI control panel core 4k")
    await message.reply_photo(photo=top_img, caption=menu_text, reply_markup=keyboard)

# ==========================================
# 🧹 11. SERVER STORAGE CLEANER (Anti-Crash)
# ==========================================
@bot.on_message(filters.command("clearcache") & filters.user(8853897167))
async def clear_server_cache(client, message: Message):
    m = await message.reply_text("🧹 **Clearing VPS Storage Cache...**")
    folders_to_clear = ["downloads", "cache", "__pycache__"]
    cleared_count = 0
    for folder in folders_to_clear:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                cleared_count += 1
            except:
                pass
    await m.edit_text(f"✅ **VPS Storage Trick Applied!**\n\n🗑️ Successfully deleted {cleared_count} junk/cache folders. Storage is now optimized.")
        
