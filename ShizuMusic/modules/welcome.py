# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#                  4K ANIME WELCOME GREETINGS
# ═══════════════════════════════════════════════════════════════

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot
from ShizuMusic.modules.ai import send_4k_card

def get_welcome_kb(bot_username: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 𝐀𝐃𝐃 𝐌𝐄", url=f"https://t.me/{bot_username}?startgroup=true"),
            InlineKeyboardButton("👑 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER"),
        ]
    ])

@bot.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    bot_me = await client.get_me()
    for member in message.new_chat_members:
        if member.id == bot_me.id:
            continue
            
        user_mention = member.mention
        chat_title = message.chat.title or "Our Group"
        
        welcome_caption = (
            f"🎉 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {chat_title.upper()}** 🎉\n\n"
            f"👋 Hey {user_mention}, group mein aapka swagat hai!\n\n"
            f"┏━━━━━━━━━━━━━━━━━━━⧫\n"
            f"┠ 🎵 **24/7 Lag-Free Music:** `/play`\n"
            f"┠ 🤖 **Smart AI & 4K Art:** `/aimenu`\n"
            f"┠ 📥 **Fast Downloader:** `/dl`\n"
            f"┗━━━━━━━━━━━━━━━━━━━⧫\n\n"
            f"💌 Powered by @MGB_NOT_FREE"
        )
        
        await send_4k_card(
            message=message,
            status_msg=None,
            prompt_img="cute anime girl smiling welcoming cherry blossom 4k",
            caption=welcome_caption,
            reply_markup=get_welcome_kb(bot_me.username)
        )

@bot.on_message(filters.command(["welcome"], prefixes=["/", "!", "."]))
async def test_welcome_cmd(client, message: Message):
    m = await message.reply_text("🌸 **Generating 4K Welcome Card...**")
    bot_me = await client.get_me()
    chat_title = message.chat.title or "MGB VIP Lounge"
    welcome_caption = (
        f"🎉 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {chat_title.upper()}** 🎉\n\n"
        f"👋 Hey {message.from_user.mention}, group mein aapka swagat hai!\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━⧫\n"
        f"┠ 🎵 **24/7 Lag-Free Music:** `/play`\n"
        f"┠ 🤖 **Smart AI & 4K Art:** `/aimenu`\n"
        f"┠ 📥 **Fast Downloader:** `/dl`\n"
        f"┗━━━━━━━━━━━━━━━━━━━⧫\n\n"
        f"💌 Powered by @MGB_NOT_FREE"
    )
    await send_4k_card(
        message=message,
        status_msg=m,
        prompt_img="cute anime girl welcoming neon aesthetic 4k",
        caption=welcome_caption,
        reply_markup=get_welcome_kb(bot_me.username)
    )
    
