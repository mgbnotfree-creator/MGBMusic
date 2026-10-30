import io, random, urllib.parse, aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot

async def get_welcome_image():
    prompt = "cute anime girl welcoming neon aesthetic cherry blossom 4k"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed={random.randint(100,99999)}&width=1024&height=1024&nologo=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    bio = io.BytesIO(await resp.read())
                    bio.name = "welcome.jpg"
                    return bio
    except: pass
    return url

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    bot_id = (await client.get_me()).id
    for member in message.new_chat_members:
        if member.id == bot_id: continue
        caption = (
            f"🎉 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {message.chat.title}** 🎉\n\n"
            f"👋 Hey {member.mention}, group mein aapka swagat hai!\n\n"
            f"┠ 🎵 **Music:** `/play`\n"
            f"┠ 🤖 **AI Features:** `/aimenu`\n"
            f"┠ 📥 **Downloader:** `/dl`\n\n"
            f"💌 Powered by @MGB_NOT_FREE"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
        img = await get_welcome_image()
        try:
            await message.reply_photo(photo=img, caption=caption, reply_markup=kb)
        except Exception:
            await message.reply_text(caption, reply_markup=kb)

@bot.on_message(filters.command(["welcome"], prefixes=["/", "!", "."]))
async def test_welcome(client, message: Message):
    m = await message.reply_text("🌸 **Generating Welcome Card...**")
    caption = (
        f"🎉 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {message.chat.title}** 🎉\n\n"
        f"👋 Hey {message.from_user.mention}, group mein aapka swagat hai!\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")]])
    img = await get_welcome_image()
    try:
        await message.reply_photo(photo=img, caption=caption, reply_markup=kb)
        await m.delete()
    except Exception:
        await m.edit_text(caption, reply_markup=kb)
