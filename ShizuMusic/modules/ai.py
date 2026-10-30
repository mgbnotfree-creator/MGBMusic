import io, random, urllib.parse, aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

# ==========================================
# 🎨 POLLINATIONS AI IMAGE API (Double Guarantee)
# ==========================================
async def get_pollinations_image(prompt):
    clean_prompt = f"{prompt}, masterpiece, highly detailed, 4k resolution, aesthetic anime"
    encoded = urllib.parse.quote(clean_prompt)
    seed = random.randint(1000, 999999)
    url = f"https://image.pollinations.ai/prompt/{encoded}?seed={seed}&width=1024&height=1024&nologo=true"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    bio = io.BytesIO(await resp.read())
                    bio.name = "pollinations.jpg"
                    return bio
    except Exception:
        pass
    return url 

# ==========================================
# 🧠 POLLINATIONS TEXT API (Strict & Clean)
# ==========================================
async def get_pollinations_text(prompt, sys_prompt):
    enc_prompt = urllib.parse.quote(prompt)
    enc_sys = urllib.parse.quote(sys_prompt)
    url = f"https://text.pollinations.ai/{enc_prompt}?model=openai&system={enc_sys}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    return (await resp.text()).strip()[:800]
    except Exception:
        pass
    return "❌ Server busy! Thodi der baad try karein."

# ==========================================
# 🖼️ UNIVERSAL SENDER WITH STYLIST EMOJIS
# ==========================================
async def send_ai_card(message: Message, status_msg: Message, prompt_img: str, caption: str):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    img = await get_pollinations_image(prompt_img)
    
    try:
        if img: await message.reply_photo(photo=img, caption=caption, reply_markup=kb)
        else: await message.reply_text(caption, reply_markup=kb)
        if status_msg: await status_msg.delete()
    except Exception:
        if status_msg: await status_msg.edit_text(caption, reply_markup=kb)
        else: await message.reply_text(caption, reply_markup=kb)

# ==========================================
# 🤖 ALL AI COMMANDS
# ==========================================
@bot.on_message(filters.command(["aimenu", "aihelp"], prefixes=["/", "!", "."]))
async def ai_menu_cmd(client, message: Message):
    m = await message.reply_text("✨ **Loading MGB 4K AI Menu...**")
    txt = "👑 **MGB NOT FREE CODER - AI MENU** 👑\n\n✦ **AI Features:**\n┠ `/ask` - Smart AI Chat\n┠ `/draw` - 4K HD Images\n┠ `/speak` - Indian Girl Voice Note\n┠ `/baba` - Future Predictor\n┠ `/meme` - Dank Memes\n┠ `/flirt` - Love Shayari\n┗ `/promo` - VIP Banner\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, "cyberpunk aesthetic anime girl hacker glowing 4k", txt)

@bot.on_message(filters.command(["ask", "ai", "chat"], prefixes=["/", "!", "."]))
async def ai_chat(client, message: Message):
    if len(message.command) < 2: return await message.reply_text("✦ `/ask [sawal]` likhein.")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🧠 **MGB AI answer nikal raha hai...**")
    ans = await get_pollinations_text(query, "You are a smart AI. Answer accurately in natural Hinglish. NO markdown tables or weird symbols.")
    caption = f"𓆩🤖𓆪 **MGB ADVANCED AI:**\n\n💬 **Sawal:** `{query}`\n\n{ans}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, f"anime conceptual art {query}", caption)

@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def ai_draw(client, message: Message):
    if len(message.command) < 2: return await message.reply_text("✦ `/draw [name]` likhein.")
    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **MGB 4K Image ban rahi hai... Please Wait!**")
    caption = f"🎨 **MGB 4K AI ART**\n\n✨ **Prompt:** `{prompt}`\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, prompt, caption)

@bot.on_message(filters.command(["speak", "tts", "voice"], prefixes=["/", "!", "."]))
async def ai_speak(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✦ **Indian Girl Voice ke liye likhein:** `/speak Hello kaise ho?`")
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🎙️ **Indian Girl Voice Note record ho rahi hai...** 🌸")
    
    ans = await get_pollinations_text(query, "You are a sweet Indian girl. Reply in 1-2 sweet sentences in Hinglish.")
    
    caption = (
        f"🎙️ **MGB INDIAN GIRL VOICE** 🌸\n\n"
        f"🗣️ **Aapka Sawal:** `{query}`\n"
        f"💬 **Ladki ka Jawab:** `{ans}`\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    
    try:
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(ans[:200])}&tl=hi-IN&client=tw-ob"
        await message.reply_audio(audio=tts_url, caption=caption, title="Indian Girl Voice Note", performer="MGB AI Girl", reply_markup=kb)
        await m.delete()
    except Exception:
        await m.edit_text(caption, reply_markup=kb)

@bot.on_message(filters.command(["meme", "joke"], prefixes=["/", "!", "."]))
async def ai_meme(client, message: Message):
    topic = message.text.split(None, 1)[1] if len(message.command) > 1 else "student and coding"
    m = await message.reply_text("🎭 **MGB Meme Zone meme dhoondh raha hai...**")
    ans = await get_pollinations_text(f"Funny Hinglish joke about {topic}", "Write exactly ONE short funny Hinglish joke. NO LABELS like 'Caption:' or 'Result:'. Just pure funny text.")
    caption = f"🎭 **MGB MEME ZONE** 🎭\n\n{ans}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, f"funny dank meme reaction {topic}", caption)

@bot.on_message(filters.command(["flirt", "shayari"], prefixes=["/", "!", "."]))
async def ai_flirt(client, message: Message):
    topic = message.text.split(None, 1)[1] if len(message.command) > 1 else "true love"
    m = await message.reply_text("🍷 **MGB Shayari likh raha hai...**")
    ans = await get_pollinations_text(f"Romantic Hinglish shayari about {topic}", "Write exactly 4 lines of romantic Hinglish shayari with aesthetic emojis. NO extra text.")
    caption = f"🍷 **MGB SHAYARI** 🍷\n\n{ans}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, "romantic anime couple aesthetic sunset", caption)

@bot.on_message(filters.command(["baba", "future"], prefixes=["/", "!", "."]))
async def ai_baba(client, message: Message):
    if len(message.command) < 2: return await message.reply_text("✦ `/baba [sawal]` likhein.")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("📿 **MGB Baba dhyaan laga rahe hain...**")
    ans = await get_pollinations_text(query, "You are a funny Indian Astrologer. Answer in 3 short sentences in Hinglish. Start with 'Vats!'. NO weird labels.")
    caption = f"𓆩♛𓆪 **MGB BABA BHAWISHYAWANI** 𓆩♛𓆪\n\n🗣️ **Sawal:** `{query}`\n\n🧘‍♂️ **Jawab:** {ans}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_ai_card(message, m, "fortune teller magic glowing crystal ball anime", caption)
        
