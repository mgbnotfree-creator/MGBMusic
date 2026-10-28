import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# 1. 5 बहुत ही खूबसूरत वेलकम इमेजेज (बॉट हर बार एक नई फोटो भेजेगा)
WELCOME_MEDIA = [
    "https://graph.org/file/e50ded8572d76cf86256b-5c067cde3b2e25017c.jpg",
    "https://telegra.ph/file/32b0c30953a9cd8ea265a.jpg",
    "https://telegra.ph/file/82633010b9fdb823ddf81.jpg",
    "https://telegra.ph/file/8b1e42817ce8c94622c81.jpg",
    "https://telegra.ph/file/71f652b415b3c5825cfd3.jpg"
]

@Client.on_message(filters.new_chat_members & filters.group)
async def advanced_welcome(client: Client, message: Message):
    for member in message.new_chat_members:
        # अगर बॉट खुद ऐड हुआ हो, तो उसे इग्नोर करे
        if member.id == client.me.id:
            continue
        
        # ग्रुप के टोटल मेंबर्स की गिनती निकालना
        try:
            count = await client.get_chat_members_count(message.chat.id)
        except Exception:
            count = "Unknown"

        # यूज़र का Username निकालना (अगर न हो तो "No Username" लिखेगा)
        username = f"@{member.username}" if member.username else "No Username"
        
        # 2. एकदम प्रीमियम और खूबसूरत टेक्स्ट डिज़ाइन (Aesthetic Layout)
        welcome_text = (
            f"✧ ━━━━━━ ❖ ━━━━━━ ✧\n"
            f" 🪷 **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏** 🪷\n"
            f"✧ ━━━━━━ ❖ ━━━━━━ ✧\n\n"
            f"👤 **𝐍𝐚𝐦𝐞:** {member.mention}\n"
            f"📛 **𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:** {username}\n"
            f"🆔 **𝐔𝐬𝐞𝐫 𝐈𝐃:** `{member.id}`\n\n"
            f"🏫 **𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞:** {message.chat.title}\n"
            f"📊 **𝐓𝐨𝐭𝐚𝐥 𝐌𝐞𝐦𝐛𝐞𝐫𝐬:** {count}\n\n"
            f"✧ ━━━━━━ ❖ ━━━━━━ ✧\n"
            f"🔖 **𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲:** [𝐌𝐆𝐁 𝐍𝐎𝐓 𝐅𝐑𝐄𝐄 𝐂𝐎𝐃𝐄𝐑](https://t.me/MGB_CODER)"
        )
        
        # 3. एडवांस बटन लेआउट (2 ऊपर और 1 नीचे)
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 𝐔𝐩𝐝𝐚𝐭𝐞𝐬", url="https://t.me/RIYA_MUSIC_BOT_786"),
                InlineKeyboardButton("💬 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/MGB_CODER")
            ],
            [
                InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
            ]
        ])
        
        # रैंडम फोटो चुनना
        random_img = random.choice(WELCOME_MEDIA)
        
        try:
            # शानदार फोटो, टेक्स्ट और बटन्स के साथ मैसेज भेजना
            await message.reply_photo(
                photo=random_img,
                caption=welcome_text,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Advanced Welcome Error: {e}")
          
