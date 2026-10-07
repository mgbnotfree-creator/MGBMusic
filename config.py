"""
config.py — All environment variables in one place.
Copy sample.env → .env and fill in your values.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Required ──────────────────────────────────────────────────────────────────
API_ID          = int(os.environ["API_ID"])
API_HASH        = os.environ["API_HASH"]
BOT_TOKEN       = os.environ["BOT_TOKEN"]
STRING_SESSION  = os.environ["STRING_SESSION"]
MONGO_DB_URL    = os.environ["MONGO_DB_URL"]
OWNER_ID        = int(os.environ["OWNER_ID"])

# ── Optional ──────────────────────────────────────────────────────────────────
BOT_NAME         = os.getenv("BOT_NAME", "MGB NOT FREE CODER")
BOT_LINK         = os.getenv("BOT_LINK", "https://t.me/MGB_CODER")
UPDATES_CHANNEL  = os.getenv("UPDATES_CHANNEL", "https://t.me/RIYA_MUSIC_BOT_786")
SUPPORT_GROUP    = os.getenv("SUPPORT_GROUP", "https://t.me/MGB_CODER")
LOGGER_ID        = int(os.getenv("LOGGER_ID", "-1004438399718"))
PING_IMG_URL     = os.getenv("PING_IMG_URL", "https://files.catbox.moe/ddzvc0.jpg")
SESSION_NAME     = os.getenv("SESSION_NAME", "ShizuMusic")
PORT             = int(os.getenv("PORT", 10000))

# ── API config ────────────────────────────────────────────────────────────────
YT_API_URL        = os.environ.get("YT_API_URL", "https://shrutibots.site")
YT_API_KEY        = os.environ.get("YT_API_KEY", "ShrutiBotsNOexqASVgg7z5F4ikHBT")  # Get from @SHRUTIAPIBOT on Telegram
DOWNLOAD_DIR          = "downloads"
YT_TOKEN_TIMEOUT  = 10    # seconds — fetch download token
YT_STREAM_TIMEOUT = 900   # 15 min  — stream long songs

#── Start ───────────────────────────────────────────────────────────────────────
START_PHOTOS = [
    "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg"
]

# ── Limits ────────────────────────────────────────────────────────────────────
MAX_DURATION_SECONDS = 10800   # 3 hours
QUEUE_LIMIT          = 20
COOLDOWN             = 10     # seconds between /play per chat

# ── Playlist limits ───────────────────────────────────────────────────────────
PLAYLIST_LIMIT       = 10     # playlists per user
PLAYLIST_SONG_LIMIT  = 50     # songs per playlist
