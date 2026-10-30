# ═══════════════════════════════════════════════════════════════
#                     🎵 MGB NOT FREE CODER
#                  ULTRA HD 4K PROMO MODULE
# ═══════════════════════════════════════════════════════════════

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from ShizuMusic import bot
from ShizuMusic.modules.ai import send_4k_card

@bot.on_message(filters.command(["promo", "promotion"], prefixes=["/", "!", "."]))
async def promo_command(client, message: Message):
    m = await message.reply_text("💎 **MGB 4K Promo Banner taiyar ho raha hai...** ✨")
    
    bot_me = await client.get_me()
    bot_username = bot_me.username
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🂡 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/MGB_CODER")],
        [
            InlineKeyboardButton("𓆩♛𓆪 𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/RIYA_MUSIC_BOT_786"),
            InlineKeyboardButton("☒ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url="https://t.me/MGB_CODER"),
        ],
        [
            InlineKeyboardButton("🦅 𝐀𝐝𝐝 𝐌𝐞 🦅", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ])
    
    promo_caption = (
        "👑 **MGB NOT FREE CODER** 👑\n\n"
        "✨ `Premium Music Bots` 🎶 | `AI Bots` 🤖 | `Render & VPS Deployment` 🚀 | `Custom APIs` 🌐\n\n"
        "💬 `Aur bhi vikalp` — **speed, stability aur personalization ka perfect mix.**\n"
        "🔗 **DM karein abhi:** 🚀\n\n"
        "🔥 **Your bots, your style** — `upgrade your game` now!\n\n"
        "💌 Powered by @MGB_NOT_FREE"
    )
    
    await send_4k_card(
        message=message,
        status_msg=m,
        prompt_img="stylish anime girl cyberpunk neon luxury music dj 4k",
        caption=promo_caption,
        reply_markup=keyboard
    )
    
