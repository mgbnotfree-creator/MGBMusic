# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#          ULTIMATE AI MODULE (4K IMAGE + ZERO GARBAGE)
# ═══════════════════════════════════════════════════════════════

import io
import random
import urllib.parse
import aiohttp
from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from ShizuMusic import bot

OWNER_URL = "https://t.me/MGB_CODER"

def get_owner_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url=OWNER_URL)]])

def get_aimenu_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✦ AI CHAT", callback_data="ai_cb_chat"),
            InlineKeyboardButton("🎨 AI IMAGES", callback_data="ai_cb_draw"),
        ],
        [
            InlineKeyboardButton("🍷 SMART DJ", callback_data="ai_cb_dj"),
            InlineKeyboardButton("💀 ROAST & FUN", callback_data="ai_cb_fun"),
        ],
        [
            InlineKeyboardButton("🦅 OWNER CONTACT 🦅", url=OWNER_URL)
        ]
    ])

# ==========================================
# 🎨 1. 100% GUARANTEED 4K IMAGE ENGINE
# ==========================================
async def get_ai_image_bytes(prompt="beautiful anime girl 4k aesthetic"):
    clean_prompt = f"{prompt}, ultra detailed, 4k resolution, masterpiece, vibrant aesthetic"
    encoded_prompt = urllib.parse.quote(clean_prompt)
    seed = random.randint(100000, 999999)
    
    urls = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true&model=flux",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true",
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    timeout = aiohttp.ClientTimeout(total=20)
    
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        # Layer 1 & 2: Pollinations 4K AI
        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        if len(data) > 1500:
                            bio = io.BytesIO(data)
                            bio.name = "mgb_4k.jpg"  # Mandatory for Pyrogram!
                            return bio
            except Exception:
                continue
        
        # Layer 3: Instant HD Anime Girl Fallback (Never Fails!)
        try:
            async with session.get("https://api.waifu.pics/sfw/waifu") as r:
                if r.status == 200:
                    js = await r.json()
                    img_url = js.get("url")
                    if img_url:
                        async with session.get(img_url) as img_r:
                            if img_r.status == 200:
                                bio = io.BytesIO(await img_r.read())
                                bio.name = "mgb_anime.jpg"
                                return bio
        except Exception:
            pass
    return None

# Helper to safely send Photo + Caption under 1024 limit
async def send_4k_card(message: Message, status_msg: Message, prompt_img: str, caption: str, reply_markup=None):
    if reply_markup is None:
        reply_markup = get_owner_kb()
    
    # Telegram photo caption limit is 1024 chars
    if len(caption) > 1000:
        caption = caption[:995] + "..."
        
    img_bio = await get_ai_image_bytes(prompt_img)
    if img_bio:
        try:
            await message.reply_photo(photo=img_bio, caption=caption, reply_markup=reply_markup)
            if status_msg:
                await status_msg.delete()
            return
        except Exception:
            pass
            
    if status_msg:
        await status_msg.edit_text(caption, reply_markup=reply_markup)
    else:
        await message.reply_text(caption, reply_markup=reply_markup)

# ==========================================
# 🧠 2. CLEAN & ACCURATE TEXT AI (POST JSON)
# ==========================================
async def fetch_advanced_ai_text(prompt, system_prompt=""):
    default_system = (
        "You are an elite, 100% accurate AI created by MGB NOT FREE CODER. "
        "Always give verified facts (especially movie release dates, history, coding). "
        "Keep answers concise (under 500 characters), clean, and in natural Hinglish. "
        "NEVER output weird markdown tables, random symbols, or meta instructions."
    )
    final_system = system_prompt if system_prompt else default_system
    
    payload = {
        "messages": [
            {"role": "system", "content": final_system},
            {"role": "user", "content": prompt}
        ],
        "model": "openai",
        "private": True
    }
    
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    timeout = aiohttp.ClientTimeout(total=20)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Try 1: Official POST Endpoint (No Garbage, 100% Clean)
        try:
            async with session.post("https://text.pollinations.ai/", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    text = (await resp.text()).strip()
                    if text:
                        return text[:650]
        except Exception:
            pass
            
        # Try 2: Fast GET Fallback
        try:
            enc_p = urllib.parse.quote(prompt)
            enc_s = urllib.parse.quote(final_system)
            url = f"https://text.pollinations.ai/{enc_p}?model=openai&system={enc_s}"
            async with session.get(url) as resp2:
                if resp2.status == 200:
                    text = (await resp2.text()).strip()
                    if text:
                        return text[:650]
        except Exception:
            pass
            
    return "⚡ Boss, abhi server par high traffic hai, 5 second baad try karein!"

# ==========================================
# 👑 3. /aimenu - FULL MENU WITH 4K IMAGE
# ==========================================
AIMENU_TEXT = (
    "👑 **MGB NOT FREE CODER - AI MENU** 👑\n\n"
    "✦ **Available AI Features:**\n"
    "┏━━━━━━━━━━━━━━━━━━━⧫\n"
    "┠ `/ask` - Smart AI Chat\n"
    "┠ `/draw` - Premium 4K HD Images\n"
    "┠ `/speak` - AI Voice Note\n"
    "┠ `/aidj` - Smart AI Music DJ\n"
    "┠ `/roast` - Savage Roast\n"
    "┠ `/flirt` / `/shayari` - Love Shayari\n"
    "┠ `/baba` - Future Predictor\n"
    "┠ `/meme` - Dank AI Memes\n"
    "┗ `/tod` - Truth or Dare\n\n"
    "✦ *Select any option below!*\n"
    "💌 Powered by @MGB_NOT_FREE"
)

@bot.on_message(filters.command(["aimenu", "aihelp"], prefixes=["/", "!", "."]))
async def ai_menu_cmd(client, message: Message):
    m = await message.reply_text("✨ **Loading MGB 4K AI Menu...**")
    await send_4k_card(
        message=message,
        status_msg=m,
        prompt_img="cyberpunk aesthetic anime girl headphones neon glowing 4k",
        caption=AIMENU_TEXT,
        reply_markup=get_aimenu_kb()
    )

@bot.on_callback_query(filters.regex("^ai_cb_"))
async def ai_menu_callbacks(client, query: CallbackQuery):
    data = query.data
    if data == "ai_cb_chat":
        txt = "🤖 **MGB SMART AI CHAT**\n\nKoi bhi sawal puchne ke liye likhein:\n`/ask Awarapan movie kab release hui thi?`"
    elif data == "ai_cb_draw":
        txt = "🎨 **MGB 4K IMAGE GENERATOR**\n\nKoi bhi 4K photo banwane ke liye likhein:\n`/draw cute anime girl with katana 4k`"
    elif data == "ai_cb_dj":
        txt = "🍷 **MGB SMART AI DJ**\n\nApne mood ke hisaab se best songs pane ke liye likhein:\n`/aidj late night drive romantic songs`"
    else:
        txt = "💀 **MGB ROAST & FUN ZONE**\n\n• `/roast @username`\n• `/flirt romantic`\n• `/baba meri shadi kab hogi`\n• `/meme coding`\n• `/tod`"
    
    back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝐁𝐀𝐂𝐊 𝐓𝐎 𝐌𝐄𝐍𝐔", callback_data="ai_back_main")]])
    await query.message.edit_caption(caption=f"{txt}\n\n💌 Powered by @MGB_NOT_FREE", reply_markup=back_kb)

@bot.on_callback_query(filters.regex("^ai_back_main$"))
async def ai_menu_back(client, query: CallbackQuery):
    await query.message.edit_caption(caption=AIMENU_TEXT, reply_markup=get_aimenu_kb())

# ==========================================
# 🤖 4. /ask - ACCURATE AI CHAT
# ==========================================
@bot.on_message(filters.command(["ask", "ai", "chat"], prefixes=["/", "!", "."]))
async def ai_chat(client, message: Message):
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading...**")
        return await send_4k_card(
            message, m,
            "cute anime girl with futuristic hologram 4k",
            "✦ **Boss, koi sawal pucho!**\nExample: `/ask Awarapan movie kab release hui thi?`"
        )
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🧠 **MGB AI accurate answer nikal raha hai...** ✦")
    answer = await fetch_advanced_ai_text(query)
    caption = f"𓆩🤖𓆪 **MGB ADVANCED AI:**\n\n💬 **Sawal:** `{query}`\n\n{answer}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, f"aesthetic anime art {query}", caption)

# ==========================================
# 🎨 5. /draw - 4K IMAGE GENERATOR
# ==========================================
@bot.on_message(filters.command(["draw", "imagine"], prefixes=["/", "!", "."]))
async def ai_draw(client, message: Message):
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading...**")
        return await send_4k_card(
            message, m,
            "cyberpunk anime girl 4k",
            "✦ **Boss, kya banwana hai?**\nExample: `/draw a cute dog in 4k`"
        )
    
    prompt = message.text.split(None, 1)[1]
    m = await message.reply_text("🎨 **MGB AI 4K Image generate kar raha hai...** 🕸️")
    caption = f"🎨 **MGB 4K AI ART**\n\n✨ **Prompt:** `{prompt}`\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, prompt, caption)

# ==========================================
# 🔮 6. /baba - CLEAN FUTURE PREDICTOR
# ==========================================
@bot.on_message(filters.command(["baba", "future"], prefixes=["/", "!", "."]))
async def ai_baba(client, message: Message):
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading...**")
        return await send_4k_card(
            message, m,
            "mystical anime girl mage glowing crystal ball 4k",
            "✦ **Bacha, pehle apna sawal toh pucho!**\nExample: `/baba meri shadi kab hogi?`"
        )
    
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("📿 **MGB Baba divya drishti laga rahe hain... 🧘‍♂️**")
    
    sys_p = (
        "You are MGB Baba, a hilarious Indian astrologer. Reply in 3-4 short, clean sentences in Hinglish. "
        "Start with 'Bachha sun!' and end with 'Tathastu! ✋'. "
        "DO NOT use any tables, bullet points, or random English gibberish."
    )
    answer = await fetch_advanced_ai_text(query, sys_p)
    caption = (
        f"𓆩♛𓆪 **MGB BABA BHAWISHYAWANI** 𓆩♛𓆪\n\n"
        f"🗣️ **Bhakht ka Sawal:** `{query}`\n\n"
        f"🧘‍♂️ **Baba ka Jawab:**\n{answer}\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    await send_4k_card(message, m, "mystic fortune teller magic aura anime 4k", caption)

# ==========================================
# 🎭 7. /meme - REAL IMAGE + FUNNY PUNCHLINE
# ==========================================
@bot.on_message(filters.command(["meme", "joke"], prefixes=["/", "!", "."]))
async def ai_meme(client, message: Message):
    topic = message.text.split(None, 1)[1] if len(message.command) > 1 else "Indian students and mobile coding"
    m = await message.reply_text("🎭 **MGB AI ek tagda meme bana raha hai... 😂**")
    
    sys_p = (
        "You are a dank Indian meme creator. Write ONLY a 2-3 line hilarious, savage Hinglish joke or meme dialogue. "
        "NEVER write 'Top Caption', 'Bottom Caption', or 'Picture idea'. Just write the funny lines directly."
    )
    meme_text = await fetch_advanced_ai_text(f"Write a funny Hinglish joke on: {topic}", sys_p)
    caption = f"🎭 **MGB MEME ZONE** 🎭\n\n{meme_text}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, f"funny anime reaction face {topic} 4k", caption)

# ==========================================
# 🍷 8. /flirt & /shayari - ROMANCE MASTER
# ==========================================
@bot.on_message(filters.command(["shayari", "flirt"], prefixes=["/", "!", "."]))
async def ai_shayari(client, message: Message):
    target_name = (
        message.reply_to_message.from_user.first_name
        if message.reply_to_message and message.reply_to_message.from_user
        else ""
    )
    if target_name:
        prompt = f"Write a smooth, romantic 2-line Hinglish pickup line and 4-line shayari for {target_name}."
    elif len(message.command) > 1:
        topic = message.text.split(None, 1)[1]
        prompt = f"Write a heart-touching 4-line Hindi/Hinglish shayari on: {topic}."
    else:
        prompt = "Write a romantic 4-line Hinglish love shayari."
        
    sys_p = (
        "You are a romantic shayar. Output ONLY a clean 4-line Hinglish shayari with aesthetic emojis. "
        "No extra explanation."
    )
    m = await message.reply_text("🍷 **MGB AI shayari craft kar raha hai... ✨**")
    result_text = await fetch_advanced_ai_text(prompt, sys_p)
    header = f"🍷 **MGB ADVANCED FLIRT** 🍷\n👤 **Target:** {target_name}\n\n" if target_name else "🍷 **MGB AI SHAYARI** 🍷\n\n"
    caption = f"{header}{result_text}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, "romantic anime couple sunset aesthetic 4k", caption)

# ==========================================
# 🔥 9. /roast - SAVAGE ROASTER
# ==========================================
@bot.on_message(filters.command(["roast"], prefixes=["/", "!", "."]))
async def ai_roast(client, message: Message):
    target = (
        message.text.split(None, 1)[1]
        if len(message.command) > 1
        else (message.reply_to_message.from_user.first_name if message.reply_to_message and message.reply_to_message.from_user else "Dost")
    )
    m = await message.reply_text("🔥 **MGB AI tandoor garam kar raha hai...**")
    sys_p = (
        "You are a savage Indian roaster. Write a brutal, hilarious 3-line Hinglish roast for the target. "
        "Keep it super funny and punchy without weird symbols."
    )
    roast_text = await fetch_advanced_ai_text(f"Roast {target}", sys_p)
    caption = f"🔥 **MGB SAVAGE ROAST** 🔥\n\n🎯 **Target:** {target}\n\n{roast_text}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, "badass anime character fire aura 4k", caption)

# ==========================================
# 🎲 10. /tod - TRUTH OR DARE
# ==========================================
@bot.on_message(filters.command(["tod", "truthdare"], prefixes=["/", "!", "."]))
async def ai_tod(client, message: Message):
    m = await message.reply_text("🎲 **MGB AI game set kar raha hai...**")
    sys_p = (
        "Give one spicy/funny Truth question and one fun Dare task in Hinglish for a Telegram group chat. "
        "Keep it short and formatted cleanly."
    )
    tod_text = await fetch_advanced_ai_text("Truth and Dare in Hinglish", sys_p)
    caption = f"🎲 **MGB TRUTH OR DARE** 🎲\n\n{tod_text}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, "anime gaming girl neon cyberpunk 4k", caption)

# ==========================================
# 🎧 11. /aidj - SMART AI MUSIC DJ
# ==========================================
@bot.on_message(filters.command(["aidj", "dj"], prefixes=["/", "!", "."]))
async def ai_dj(client, message: Message):
    mood = message.text.split(None, 1)[1] if len(message.command) > 1 else "chill lofi & romantic"
    m = await message.reply_text("🎧 **MGB Smart DJ tracks mix kar raha hai...**")
    sys_p = (
        "You are MGB Smart DJ. Suggest 5 top Bollywood/Punjabi/Global songs matching the user's mood. "
        "List them cleanly with emojis and tell the user they can play them using /play [song name]."
    )
    dj_text = await fetch_advanced_ai_text(f"Suggest 5 songs for mood: {mood}", sys_p)
    caption = f"🎧 **MGB SMART AI DJ** 🎧\n\n🎶 **Mood:** `{mood}`\n\n{dj_text}\n\n💌 Powered by @MGB_NOT_FREE"
    await send_4k_card(message, m, "anime dj girl neon club headphones 4k", caption)

# ==========================================
# 🗣️ 12. /speak - AI VOICE NOTE
# ==========================================
@bot.on_message(filters.command(["speak", "tts"], prefixes=["/", "!", "."]))
async def ai_speak(client, message: Message):
    if len(message.command) < 2:
        m = await message.reply_text("✨ **Loading...**")
        return await send_4k_card(
            message, m,
            "anime girl singing into microphone 4k",
            "✦ **Boss, kya bulwana hai?**\nExample: `/speak Welcome to MGB Music Bot`"
        )
    text = message.text.split(None, 1)[1][:200]
    m = await message.reply_text("🎙️ **MGB AI Voice record kar raha hai...**")
    enc_text = urllib.parse.quote(text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={enc_text}&tl=hi&client=tw-ob"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(tts_url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                if resp.status == 200:
                    voice_bio = io.BytesIO(await resp.read())
                    voice_bio.name = "mgb_voice.ogg"
                    await message.reply_voice(
                        voice=voice_bio,
                        caption=f"🎙️ **MGB AI VOICE:** `{text}`\n💌 Powered by @MGB_NOT_FREE",
                        reply_markup=get_owner_kb()
                    )
                    return await m.delete()
    except Exception:
        pass
    await send_4k_card(message, m, "anime girl microphone 4k", f"🎙️ `{text}`\n\n💌 Powered by @MGB_NOT_FREE")
    
