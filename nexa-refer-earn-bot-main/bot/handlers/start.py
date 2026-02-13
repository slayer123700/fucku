from datetime import datetime
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.main import app
from bot.database import users
from bot.config import START_IMAGE, MUST_JOIN_IMAGE
from bot.keyboards.inline import must_join_kb
from bot.keyboards.reply import home_reply_kb
from bot.utils import is_user_joined

# ───────────────────────────────────────────────
# INLINE BUTTON FOR PROOFS
# ───────────────────────────────────────────────
proof_btn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("✨ Vɪᴇᴡ Pʀᴏᴏғs ✨", url="https://t.me/NexaProof")]]
)

# ───────────────────────────────────────────────
# ANIMATED WELCOME LOADER
# ───────────────────────────────────────────────
async def animated_welcome(message):
    frames = [
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▱▱▱▱▱",
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▰▱▱▱▱",
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▰▰▱▱▱",
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▰▰▰▱▱",
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▰▰▰▰▱",
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ**\n\n▰▰▰▰▰",
    ]

    msg = await message.reply(frames[0])
    for frame in frames[1:]:
        try:
            await msg.edit_text(frame)
        except MessageNotModified:
            pass
        await asyncio.sleep(0.35)
    return msg

# ───────────────────────────────────────────────
# QUOTED-STYLE START MESSAGE
# ───────────────────────────────────────────────
quoted_caption = (
    "**✨ Wᴇʟᴄᴏᴍᴇ Tᴏ Nᴇxᴀ Rᴇғᴇʀ & Eᴀʀɴ ⭐**\n\n"
    "**💸 1 Rᴇғᴇʀ = 1 ⭐**\n"
    "**Dᴀɪʟʏ Bᴏɴᴜs**\n"
    "**Fᴀsᴛ Wɪᴛʜᴅʀᴀᴡs**\n\n"
    "**👇 Vɪᴇᴡ Pʀᴏᴏғs 👇**"
)

# ───────────────────────────────────────────────
# /start HANDLER
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.command("start"))
async def start_handler(_, message):
    uid = message.from_user.id
    user = message.from_user

    # ── REFERRAL ID IF EXISTS ──
    ref_id = None
    if len(message.command) > 1:
        try:
            ref_id = int(message.command[1])
        except ValueError:
            pass

    # ── CREATE USER IF NOT EXISTS ──
    users.update_one(
        {"user_id": uid},
        {
            "$setOnInsert": {
                "user_id": uid,
                "name": user.first_name,
                "username": user.username,
                "stars": 0,
                "referrals": 0,
                "join_bonus": False,
                "referred": False,
                "joined_at": datetime.utcnow(),
            }
        },
        upsert=True
    )
    user_data = users.find_one({"user_id": uid}) or {}

    # ── APPLY REFERRAL REWARD ──
    if ref_id and ref_id != uid and not user_data.get("referred"):
        ref_user = users.find_one({"user_id": ref_id})
        if ref_user:
            users.update_one({"user_id": ref_id}, {"$inc": {"stars": 1, "referrals": 1}})
            users.update_one({"user_id": uid}, {"$set": {"referred": True}})
            try:
                await app.send_message(
                    ref_id,
                    "🎉 **Rᴇғᴇʀʀᴀʟ Sᴜᴄᴄᴇss!**\n\n⭐ +1 Sᴛᴀʀ Aᴅᴅᴇᴅ"
                )
            except:
                pass

    # ── FORCE JOIN CHECK ──
    if not await is_user_joined(app, uid):
        return await message.reply_photo(
            photo=MUST_JOIN_IMAGE,
            caption=(
                "🔒 **Jᴏɪɴ Rᴇǫᴜɪʀᴇᴅ**\n\n"
                "Tᴏ Usᴇ Tʜɪs Bᴏᴛ, Jᴏɪɴ Aʟʟ Cʜᴀɴɴᴇʟs.\n\n"
                "✅ Cʟɪᴄᴋ **Vᴇʀɪғʏ Jᴏɪɴ**"
            ),
            reply_markup=must_join_kb(),
            has_spoiler=True
        )

    # ── ANIMATED LOADER ──
    loader = await animated_welcome(message)
    try:
        await loader.delete()
    except:
        pass

    # ── SEND START IMAGE WITH QUOTED CAPTION ──
    await message.reply_photo(
        photo=START_IMAGE,
        caption=quoted_caption,
        reply_markup=proof_btn,
        has_spoiler=True
    )

    # ── SEND HOME MENU ──
    await message.reply(
        "🏠 **Hᴏᴍᴇ Mᴇɴᴜ Lᴏᴀᴅᴇᴅ**",
        reply_markup=home_reply_kb()
    )

# ───────────────────────────────────────────────
# VERIFY JOIN CALLBACK
# ───────────────────────────────────────────────
@app.on_callback_query(filters.regex("^verify_join$"))
async def verify_join(_, query):
    uid = query.from_user.id

    # ── LOADER WHILE VERIFYING ──
    for text in [
        "🔍 ᴄʜᴇᴄᴋɪɴɢ ʏᴏᴜʀ ᴊᴏɪɴ",
        "🔍 ᴄʜᴇᴄᴋɪɴɢ ʏᴏᴜʀ ᴊᴏɪɴ.",
        "🔍 ᴄʜᴇᴄᴋɪɴɢ ʏᴏᴜʀ ᴊᴏɪɴ..",
        "🔐 ᴠᴇʀɪғʏɪɴɢ…",
    ]:
        try:
            await query.message.edit_text(text)
        except MessageNotModified:
            pass
        await asyncio.sleep(0.4)

    # ── VERIFY JOIN STATUS ──
    if not await is_user_joined(app, uid):
        return await query.message.edit_text(
            "❌ **Jᴏɪɴ Nᴏᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ**",
            reply_markup=must_join_kb()
        )

    # ── GIVE JOIN BONUS ──
    user_data = users.find_one({"user_id": uid}) or {}
    if not user_data.get("join_bonus"):
        users.update_one(
            {"user_id": uid},
            {"$inc": {"stars": 1}, "$set": {"join_bonus": True}}
        )
        await app.send_message(
            uid,
            "🎁 **Jᴏɪɴ Bᴏɴᴜs Uɴʟᴏᴄᴋᴇᴅ!**\n⭐ +1 Sᴛᴀʀ"
        )

    # ── CLEANUP VERIFY MESSAGE ──
    try:
        await query.message.delete()
    except:
        pass

    # ── SEND HOME MENU AFTER VERIFICATION ──
    await app.send_message(
        uid,
        "✅ **Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!**",
        reply_markup=home_reply_kb()
    )