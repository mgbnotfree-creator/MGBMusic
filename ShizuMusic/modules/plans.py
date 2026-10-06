import random
from pyrogram import filters
from pyrogram.types import Message

import config
from ShizuMusic import bot
from ShizuMusic.modules.block import user_allowed
from ShizuMusic.utils.buttons import _row, _url_btn, _tg_btn, random_style
from ShizuMusic.utils.language import chat_strings
from richgram import (
    rich_esc,
    rich_heading,
    rich_img,
    rich_note,
    rich_send,
    rich_table,
    rich_details,
    sanitize_display_name,
)

@bot.on_message(filters.command("plans") & user_allowed)
async def plans_command_handler(_, message: Message) -> None:
    uid = message.from_user.id
    name = sanitize_display_name(message.from_user.first_name)
    chat_id = message.chat.id
    
    # ── Correct Permanent Payment QR Link ───────────────────────────────────
    qr_photo = "https://graph.org/file/ec12b5f611339d0e12b68-bb2038837e496d0655.jpg"
    lang = chat_strings(chat_id)

    # ── Delete user's command message ────────────────────────────────────────
    try:
        await message.delete()
    except Exception:
        pass

    # ── Plans Data Table Headers & Rows (Updated Prices) ─────────────────────
    headers = ["💎 PLAN", "💵 PRICE", "⚡ REQUESTS / DAY"]
    rows = [
        ["Free", "Free", "100 (Default)"],
        ["Lite", "₹49", "1,500"],
        ["Basic", "₹79", "3,000"],
        ["Starter ⭐", "₹99", "5,000"],
        ["Standard", "₹199", "10,000"],
        ["Pro", "₹329", "25,000"],
        ["Business", "₹569", "50,000"],
        ["Enterprise", "₹1,099", "100,000"],
    ]

    # ── Rich UI Layout Construction ──────────────────────────────────────────
    caption = (
        rich_img(qr_photo)
        + rich_heading("🚀 API SUBSCRIPTION PLANS & PRICING", level=2)
        + rich_note(f"👋 Hello <b>{rich_esc(name)}</b>! Check out our high-speed API plans below. Scan the QR or contact us to buy/upgrade.")
        + rich_details(
            "📋 <b>Available Plans & Rate Limits</b>",
            rich_table(headers, rows),
            open=True,
        )
        + rich_note("💡 <i>After payment via QR, send the screenshot to our contact or support channel to activate your plan.</i>")
    )

    # ── Interactive Action Buttons (QR Link, Contact @MGB_NOT_FREE & Support) ──
    kb = (
        _row(
            _url_btn("📷 ᴘᴀʏᴍᴇɴᴛ ǫʀ", qr_photo, random_style()),
            _url_btn("💬 ᴄᴏɴᴛᴀᴄᴛ", "https://t.me/MGB_NOT_FREE", random_style()),
        )
        + _row(
            _url_btn("🍬 sᴜᴘᴘᴏʀᴛ", config.SUPPORT_GROUP, random_style()),
            _tg_btn("⌯ ᴄʟᴏsᴇ ⌯", "close_player", "danger")
        )
    )

    try:
        await rich_send(bot, chat_id, caption + kb)
    except Exception as e:
        print(f"[plans_command_handler] Error: {e}")
