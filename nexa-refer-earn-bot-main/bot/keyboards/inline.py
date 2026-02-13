from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import FORCE_CHANNELS


# ───────────────────────────────────────────────
# 🔒 MUST JOIN KEYBOARD
# • 2 join buttons per row
# • Channel name hidden
# • Clean minimal UI
# ───────────────────────────────────────────────
def must_join_kb():
    buttons = []
    row = []

    for ch in FORCE_CHANNELS:
        channel = ch.replace("@", "").replace("https://t.me/", "")

        row.append(
            InlineKeyboardButton(
                text="🔗 Jᴏɪɴ",
                url=f"https://t.me/{channel}"
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ Vᴇʀɪғʏ Jᴏɪɴ",
                callback_data="verify_join"
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


# ───────────────────────────────────────────────
# 🏠 HOME INLINE MENU (NO STAR)
# ───────────────────────────────────────────────
def home_kb():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👥 Rᴇғᴇʀ & Eᴀʀɴ", callback_data="refer"),
                InlineKeyboardButton("💼 Wᴀʟʟᴇᴛ", callback_data="wallet"),
            ],
            [
                InlineKeyboardButton("🎁 Dᴀɪʟʏ Bᴏɴᴜs", callback_data="daily_bonus"),
                InlineKeyboardButton("📤 Wɪᴛʜᴅʀᴀᴡ", callback_data="withdraw"),
            ],
            [
                InlineKeyboardButton("🏆 Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ", callback_data="leaderboard"),
            ],
            [
                InlineKeyboardButton("📝 Fᴇᴇᴅʙᴀᴄᴋ", callback_data="feedback"),
                InlineKeyboardButton("📞 Sᴜᴘᴘᴏʀᴛ", callback_data="support"),
            ],
        ]
    )


# ───────────────────────────────────────────────
# 📝 FEEDBACK RATING (NO STAR ICONS)
# ───────────────────────────────────────────────
def feedback_rating_kb():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("1️⃣", callback_data="rate_1"),
                InlineKeyboardButton("2️⃣", callback_data="rate_2"),
                InlineKeyboardButton("3️⃣", callback_data="rate_3"),
            ],
            [
                InlineKeyboardButton("4️⃣", callback_data="rate_4"),
                InlineKeyboardButton("5️⃣", callback_data="rate_5"),
            ],
        ]
    )


# ───────────────────────────────────────────────
# 🔙 ADMIN BACK BUTTON
# ───────────────────────────────────────────────
def admin_back_kb():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Bᴀᴄᴋ",
                    callback_data="admin_back"
                )
            ]
        ]
    )