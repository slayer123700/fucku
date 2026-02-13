from datetime import date, timedelta
from datetime import datetime, date
from zoneinfo import ZoneInfo  
from pyrogram.enums import ParseMode
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from datetime import datetime, timezone, timedelta
import asyncio
from bson import ObjectId
from pymongo import ReturnDocument

from bot.main import app
from bot.database import users, withdraws
from bot.keyboards.reply import home_reply_kb
from bot.config import (
    BOT_USERNAME,
    ADMIN_IDS,
    ADMIN_LOG_GROUP,
    FEEDBACK_IMAGE,
)

# ───────────────────────────────────────────────
# ui constants
# ───────────────────────────────────────────────
LINE = "━━━━━━━━━━━━━━━━━━"
ALLOWED_WITHDRAW = [15, 25, 50, 75, 100, 300, 400]
MENU_BTNS = ("👥", "⭐", "🎁", "📤", "📝", "📞", "🏆")

MIN_WITHDRAW = 15

# ───────────────────────────────────────────────
# helpers (cinematic + ultra safe)
# ───────────────────────────────────────────────

IST = timezone(timedelta(hours=5, minutes=30))

def ts() -> str:
    """Return formatted India (IST) timestamp."""
    return datetime.now(IST).strftime("%d %b %Y • %I:%M %p")


# ───────────────────────────────────────────────
# safe_send — flood + peer resolve safe
# ───────────────────────────────────────────────
async def safe_send(chat_id: int, text: str, **kwargs):
    try:
        await app.get_chat(chat_id)
        return await app.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
            **kwargs
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await safe_send(chat_id, text, **kwargs)
    except Exception as e:
        print(f"[safe_send] ⚠️ failed to send to {chat_id}: {e}")


# ───────────────────────────────────────────────
# shimmer — cinematic pulse effect
# ───────────────────────────────────────────────
async def shimmer(msg, base: str, loops: int = 6, delay: float = 0.25):
    """Animated shimmer text for cinematic effects."""
    frames = [
        f"✨ {base}",
        f"🌒 {base}",
        f"🌕 {base}",
        f"💫 {base}",
        f"🌑 {base}",
    ]

    for i in range(loops):
        try:
            await msg.edit_text(frames[i % len(frames)])
        except Exception:
            pass
        await asyncio.sleep(delay)


# ───────────────────────────────────────────────
# progress_bar — smooth progress animation
# ───────────────────────────────────────────────
async def progress_bar(msg, title: str = "processing", speed: float = 0.25):
    """Smoothly animated progress bar for processing scenes."""
    bars = [
        "▱▱▱▱▱",
        "▰▱▱▱▱",
        "▰▰▱▱▱",
        "▰▰▰▱▱",
        "▰▰▰▰▱",
        "▰▰▰▰▰"
    ]

    for bar in bars:
        try:
            await msg.edit_text(f"⏳ **{title}**\n\n`{bar}`")
        except Exception:
            pass
        await asyncio.sleep(speed)


# ───────────────────────────────────────────────
# refer & earn (cinematic + premium ui)
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.regex("^👥"))
async def refer(_, m):
    uid = m.from_user.id
    u = users.find_one({"user_id": uid}) or {}

    stars = u.get("stars", 0)
    refs = u.get("referrals", 0)
    link = f"https://t.me/{BOT_USERNAME}?start={uid}"

    # cinematic opening
    msg = await m.reply("✨ Oᴘᴇɴɪɴɢ Rᴇғᴇʀ Pᴀɴᴇʟ…")
    await shimmer(msg, "Lᴏᴀᴅɪɴɢ Rᴇᴡᴀʀᴅs")
    await progress_bar(msg, "Rᴇғᴇʀ & Eᴀʀɴ")

    # tier based on referrals (safe logic)
    if refs >= 50:
        tier = "👑 Mᴀsᴛᴇʀ Rᴇғᴇʀʀᴇʀ"
    elif refs >= 20:
        tier = "💎 Pʀᴏ Rᴇғᴇʀʀᴇʀ"
    elif refs >= 5:
        tier = "⭐ Aᴄᴛɪᴠᴇ Rᴇғᴇʀʀᴇʀ"
    else:
        tier = "🌱 Bᴇɢɪɴɴᴇʀ"

    await msg.edit_text(
        f"🌑 **Rᴇғᴇʀ & Eᴀʀɴ**\n"
        f"{LINE}\n\n"
        f"👤 Usᴇʀ Iᴅ: `{uid}`\n"
        f"👥 Rᴇғᴇʀʀᴀʟs: `{refs}`\n"
        f"🎁 Rᴇᴡᴀʀᴅ: `1 ⭐ / Rᴇғᴇʀ`\n"
        f"⭐ Tᴏᴛᴀʟ Sᴛᴀʀs: `{stars}`\n"
        f"🏷️ Lᴇᴠᴇʟ: `{tier}`\n\n"
        f"{LINE}\n"
        f"🔗 Yᴏᴜʀ Rᴇғᴇʀ Lɪɴᴋ:\n"
        f"`{link}`\n\n"
        f"🕒 {ts()}",
        reply_markup=home_reply_kb()
    )


# ───────────────────────────────────────────────
# wallet (cinematic + luxury ui)
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.regex("^⭐"))
async def wallet(_, m):
    uid = m.from_user.id
    u = users.find_one({"user_id": uid}) or {}

    stars = u.get("stars", 0)
    refs = u.get("referrals", 0)

    # cinematic opening
    msg = await m.reply("💼 Oᴘᴇɴɪɴɢ Wᴀʟʟᴇᴛ…")
    await shimmer(msg, "Sʏɴᴄɪɴɢ Bᴀʟᴀɴᴄᴇ")
    await progress_bar(msg, "Wᴀʟʟᴇᴛ")

    # vip level (optional logic – safe default)
    if stars >= 500:
        vip = "👑 Vɪᴘ"
    elif stars >= 200:
        vip = "💎 Pʀᴇᴍɪᴜᴍ"
    else:
        vip = "⭐ Sᴛᴀɴᴅᴀʀᴅ"

    await msg.edit_text(
        f"🌑 **Yᴏᴜʀ Wᴀʟʟᴇᴛ**\n"
        f"{LINE}\n\n"
        f"👤 Usᴇʀ: `{uid}`\n"
        f"⭐ Sᴛᴀʀs: `{stars}`\n"
        f"👥 Rᴇғᴇʀʀᴀʟs: `{refs}`\n"
        f"👑 Lᴇᴠᴇʟ: `{vip}`\n\n"
        f"{LINE}\n"
        f"🕒 {ts()}",
        reply_markup=home_reply_kb()
    )


# ───────────────────────────────────────────────
# DAILY BONUS (FIXED + ATOMIC + SAFE)
# ───────────────────────────────────────────────

@app.on_message(filters.private & filters.regex("^🎁"))
async def bonus(_, m):
    uid = m.from_user.id
    today = date.today()

    u0 = users.find_one({"user_id": uid}) or {}

    last_bonus = u0.get("last_bonus")

    # normalize stored date
    if isinstance(last_bonus, str):
        last_bonus = date.fromisoformat(last_bonus)

    # already claimed today
    if last_bonus == today:
        return await m.reply(
            "⏳ **Bᴏɴᴜs Aʟʀᴇᴀᴅʏ Cʟᴀɪᴍᴇᴅ**",
            reply_markup=home_reply_kb()
        )

    msg = await m.reply("🎁 Cʜᴇᴄᴋɪɴɢ…")
    await shimmer(msg, "Vᴇʀɪғʏɪɴɢ")

    # 🔁 streak logic (reset if missed day)
    yesterday = today - timedelta(days=1)
    streak = u0.get("streak", 0)

    if last_bonus == yesterday:
        streak += 1
    else:
        streak = 1

    rewards = [1, 1, 1, 1, 2, 1, 2]
    reward = rewards[min(streak - 1, len(rewards) - 1)]

    u = users.find_one_and_update(
        {"user_id": uid},
        {
            "$set": {
                "user_id": uid,
                "last_bonus": today.isoformat(),  # ✅ ALWAYS STORE STRING
                "streak": streak
            },
            "$inc": {
                "stars": reward
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    stars = u.get("stars", 0)

    await msg.edit_text(
        "🎉 **Dᴀɪʟʏ Bᴏɴᴜs Cʟᴀɪᴍᴇᴅ**\n"
        f"{LINE}\n\n"
        f"🔥 **Sᴛʀᴇᴀᴋ:** `{streak}` Dᴀʏs\n"
        f"⭐ **+{reward} Sᴛᴀʀs**\n\n"
        f"💼 **Nᴇᴡ Bᴀʟᴀɴᴄᴇ:** `{stars} ⭐`",
        reply_markup=home_reply_kb()
    )


# ───────────────────────────────────────────────
# support (safe + animated)
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.regex("^📞"))
async def support(_, m):
    # initial cinematic entry
    msg = await m.reply("📞 Cᴏɴɴᴇᴄᴛɪɴɢ Sᴜᴘᴘᴏʀᴛ…")
    await shimmer(msg, "Rᴇᴀᴄʜɪɴɢ Tᴇᴀᴍ")

    # final UI (single edit → safe)
    await msg.edit_text(
        f"📞 **Sᴜᴘᴘᴏʀᴛ**\n"
        f"{LINE}\n\n"
        f"💬 Nᴇᴇᴅ Hᴇʟᴘ?\n"
        f"👉 @NexaSupports\n\n"
        f"🕒 {ts()}",
        reply_markup=home_reply_kb()
    )

# ───────────────────────────────────────────────
# admin: add stars (ATOMIC + SAFE)
# ───────────────────────────────────────────────
# ───────────────────────────────────────────────
# admin: add stars (ATOMIC + SAFE)
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.command("addstars"))
async def admin_add(_, m):
    if m.from_user.id not in ADMIN_IDS:
        return await m.reply("❌ not authorized")

    try:
        _, uid, amount = m.text.split()
        uid = int(uid)
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except Exception:
        return await m.reply(
            "⚙️ **usage**\n"
            "`/addstars user_id amount`"
        )

    # 🔐 ATOMIC ADD (UPSERT SAFE)
    u = users.find_one_and_update(
        {"user_id": uid},
        {
            "$inc": {"stars": amount},
            "$setOnInsert": {"user_id": uid}
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    name = await get_name(_, uid)
    balance = u.get("stars", 0)

    await m.reply(
        f"✨ **stars added**\n{LINE}\n"
        f"👤 {name}\n"
        f"user id: `{uid}`\n"
        f"added: `+{amount} ⭐`\n"
        f"new balance: `{balance} ⭐`\n\n"
        f"🕒 {ts()}"
    )

    # 🔔 notify user
    await safe_send(
        uid,
        f"✨ **stars credited**\n{LINE}\n"
        f"amount: `+{amount} ⭐`\n"
        f"balance: `{balance} ⭐`\n\n"
        f"🕒 {ts()}"
    )

    # 📢 admin log
    if ADMIN_LOG_GROUP:
        await safe_send(
            ADMIN_LOG_GROUP,
            f"➕ **admin star credit**\n{LINE}\n"
            f"👤 {name}\n"
            f"user id: `{uid}`\n"
            f"amount: `+{amount} ⭐`\n"
            f"balance: `{balance} ⭐`\n"
            f"time: {ts()}"
        )


# ───────────────────────────────────────────────
# admin: deduct stars (ATOMIC + SAFE)
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.command("deductstars"))
async def admin_deduct(_, m):
    if m.from_user.id not in ADMIN_IDS:
        return await m.reply("❌ not authorized")

    try:
        _, uid, amount = m.text.split()
        uid = int(uid)
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except Exception:
        return await m.reply(
            "⚙️ **usage**\n"
            "`/deductstars user_id amount`"
        )

    # 🔐 ATOMIC CHECK + DEDUCT
    u = users.find_one_and_update(
        {
            "user_id": uid,
            "stars": {"$gte": amount}
        },
        {
            "$inc": {"stars": -amount}
        },
        return_document=ReturnDocument.AFTER
    )

    if not u:
        return await m.reply(
            "❌ **deduction failed**\n"
            "reason: insufficient balance or user not found"
        )

    # ✅ SAFE NAME (NOT CLICKABLE)
    name = await get_name(_, uid)
    remaining = u.get("stars", 0)

    await m.reply(
        f"⚠️ **stars deducted**\n{LINE}\n"
        f"👤 {name}\n"
        f"user id: `{uid}`\n"
        f"deducted: `-{amount} ⭐`\n"
        f"remaining: `{remaining} ⭐`\n\n"
        f"🕒 {ts()}"
    )

    # optional: notify user
    await safe_send(
        uid,
        f"⚠️ **admin deduction**\n{LINE}\n"
        f"amount: `-{amount} ⭐`\n"
        f"balance: `{remaining} ⭐`\n\n"
        f"🕒 {ts()}"
    )

    # optional: admin log
    if ADMIN_LOG_GROUP:
        await safe_send(
            ADMIN_LOG_GROUP,
            f"➖ **admin star deduction**\n{LINE}\n"
            f"👤 {name}\n"
            f"user id: `{uid}`\n"
            f"amount: `-{amount} ⭐`\n"
            f"balance: `{remaining} ⭐`\n"
            f"time: {ts()}"
        )



# ───────── LEADERBOARD ─────────
@app.on_message(filters.private & filters.regex("^🏆"))
async def leaderboard_handler(_, m):
    msg = await m.reply("🏆 Fᴇᴛᴄʜɪɴɢ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ…")
    await progress_bar(msg, "Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ")

    top = list(users.find().sort("stars", -1).limit(10))
    if not top:
        return await msg.edit_text(
            "🏆 **Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ**\n"
            f"{LINE}\n\n😶‍🌫️ ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ",
            reply_markup=home_reply_kb()
        )

    CROWN_FRAMES = {
        1: ["🥇 👑", "👑 🥇", "✨ 👑", "👑 ✨"],
        2: ["🥈", "✨ 🥈", "🥈 ✨"],
        3: ["🥉", "✨ 🥉", "🥉 ✨"]
    }

    base = (
        "🏆 **Tᴏᴘ Eᴀʀɴᴇʀꜱ**\n"
        f"{LINE}\n"
        "💎 **Eʟɪᴛᴇ Rᴀɴᴋɪɴɢꜱ**\n\n"
    )

    await msg.edit_text(base, disable_web_page_preview=True)

    for frame in range(4):  # animation loops
        text = base

        for i, u in enumerate(top, 1):
            uid = u.get("user_id")
            stars = u.get("stars", 0)
            name = await get_name(_, uid)

            if i in CROWN_FRAMES:
                medal = CROWN_FRAMES[i][frame % len(CROWN_FRAMES[i])]
            else:
                medal = "🔹"

            text += (
                f"{medal} **#{i}**  {name}\n"
                f"     ⭐ **{stars}** ꜱᴛᴀʀꜱ\n\n"
            )

        await msg.edit_text(text, disable_web_page_preview=True)
        await asyncio.sleep(0.6)

    text += (
        f"{LINE}\n"
        "🔥 **Kᴇᴇᴘ Eᴀʀɴɪɴɢ • Rɪꜱᴇ Hɪɢʜᴇʀ**"
    )

    await msg.edit_text(
        text,
        reply_markup=home_reply_kb(),
        disable_web_page_preview=True
    )

# ───────── WITHDRAW PANEL ─────────
@app.on_message(filters.private & filters.regex("^📤"))
async def withdraw_panel(_, m):
    uid = m.from_user.id
    u = users.find_one({"user_id": uid}) or {}

    users.update_one(
        {"user_id": uid},
        {"$set": {"withdraw_mode": True}},
        upsert=True
    )

    msg = await m.reply("📤 Iɴɪᴛɪᴀʟɪᴢɪɴɢ…")
    await progress_bar(msg, "Wɪᴛʜᴅʀᴀᴡ")

    await msg.edit_text(
        f"🌑 **Wɪᴛʜᴅʀᴀᴡ**\n{LINE}\n"
        f"⭐ `{u.get('stars', 0)}` Bᴀʟᴀɴᴄᴇ\n\n"
        "`15 • 25 • 50 • 75 • 100 • 300 • 400`\n\n"
        "✍️ **Sᴇɴᴅ Aᴍᴏᴜɴᴛ**",
        reply_markup=home_reply_kb(),
    )


# ───────── WITHDRAW AMOUNT INPUT ─────────
@app.on_message(filters.private & filters.text)
async def withdraw_amount_handler(_, m):
    uid = m.from_user.id
    text = m.text.strip()

    u = users.find_one({"user_id": uid}) or {}

    if not u.get("withdraw_mode"):
        return

    # turn off withdraw mode immediately
    users.update_one(
        {"user_id": uid},
        {"$set": {"withdraw_mode": False}}
    )

    if not text.isdigit():
        return await m.reply("❌ **Iɴᴠᴀʟɪᴅ Aᴍᴏᴜɴᴛ**")

    amount = int(text)

    if amount < MIN_WITHDRAW:
        return await m.reply("❌ **Mɪɴɪᴍᴜᴍ Wɪᴛʜᴅʀᴀᴡ 15 ⭐**")

    if amount not in ALLOWED_WITHDRAW:
        return await m.reply("❌ **Aᴍᴏᴜɴᴛ Nᴏᴛ Aʟʟᴏᴡᴇᴅ**")

    if u.get("stars", 0) < amount:
        return await m.reply("❌ **Iɴsᴜғғɪᴄɪᴇɴᴛ Bᴀʟᴀɴᴄᴇ**")

    # deduct balance
    users.update_one(
        {"user_id": uid},
        {"$inc": {"stars": -amount}}
    )

    wd = withdraws.insert_one({
        "user_id": uid,
        "amount": amount,
        "status": "pending",
        "time": datetime.utcnow(),
    })

    kb = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Aᴘᴘʀᴏᴠᴇ", callback_data=f"wd_approve_{wd.inserted_id}"),
            InlineKeyboardButton("❌ Rᴇᴊᴇᴄᴛ", callback_data=f"wd_reject_{wd.inserted_id}")
        ]]
    )

    mention = get_mention(uid)

    if ADMIN_LOG_GROUP:
        await safe_send(
            ADMIN_LOG_GROUP,
            f"📤 **Wɪᴛʜᴅʀᴀᴡ Rᴇǫᴜᴇsᴛ**\n{LINE}\n"
            f"👤 {mention}\n"
            f"🆔 `{uid}`\n"
            f"💰 `{amount} ⭐`",
            reply_markup=kb
        )

    msg = await m.reply("⏳ Pʀᴏᴄᴇssɪɴɢ…")
    await progress_bar(msg)

    await msg.edit_text(
        f"✅ **Wɪᴛʜᴅʀᴀᴡ Sᴜʙᴍɪᴛᴛᴇᴅ**\n{LINE}\n"
        f"💰 `{amount} ⭐`\n"
        f"📌 **Pᴇɴᴅɪɴɢ**",
        reply_markup=home_reply_kb(),
    )

    # ───────── CALLBACK: WITHDRAW ACTION ─────────
@app.on_callback_query(filters.regex("^wd_"))
async def withdraw_action(_, q):
    if q.from_user.id not in ADMIN_IDS:
        return await q.answer("Not allowed", show_alert=True)

    _, action, wid = q.data.split("_")

    try:
        wid = ObjectId(wid)
    except:
        return await q.answer("Invalid request", show_alert=True)

    wd = withdraws.find_one({"_id": wid, "status": "pending"})
    if not wd:
        return await q.answer("Already processed", show_alert=True)

    uid = wd["user_id"]
    amount = wd["amount"]
    mention = get_mention(uid)

    if action == "approve":
        withdraws.update_one(
            {"_id": wid},
            {"$set": {"status": "approved", "action_time": datetime.utcnow()}}
        )

        await safe_send(
            uid,
            f"✅ **Wɪᴛʜᴅʀᴀᴡ Aᴘᴘʀᴏᴠᴇᴅ**\n{LINE}\n💰 `{amount} ⭐`"
        )

        await q.message.edit_text(
            f"✅ **Wɪᴛʜᴅʀᴀᴡ Aᴘᴘʀᴏᴠᴇᴅ**\n{LINE}\n"
            f"👤 {mention}\n💰 `{amount} ⭐`",
            disable_web_page_preview=True
        )

    elif action == "reject":
        withdraws.update_one(
            {"_id": wid},
            {"$set": {"status": "rejected", "action_time": datetime.utcnow()}}
        )

        users.update_one(
            {"user_id": uid},
            {"$inc": {"stars": amount}}
        )

        await safe_send(
            uid,
            f"❌ **Wɪᴛʜᴅʀᴀᴡ Rᴇᴊᴇᴄᴛᴇᴅ**\n{LINE}\n"
            f"💰 `{amount} ⭐`\n🔄 Rᴇғᴜɴᴅᴇᴅ"
        )

        await q.message.edit_text(
            f"❌ **Wɪᴛʜᴅʀᴀᴡ Rᴇᴊᴇᴄᴛᴇᴅ**\n{LINE}\n"
            f"👤 {mention}\n💰 `{amount} ⭐`\n🔄 Rᴇғᴜɴᴅᴇᴅ",
            disable_web_page_preview=True
        )
    # ───────── SAFE SEND ─────────
async def safe_send(chat_id, text, **kwargs):
    try:
        await app.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
            **kwargs
        )
    except Exception as e:
        print(f"[SAFE_SEND ERROR] {e}")

# IVAN TELLS THAT

def get_mention(user_id: int):
    user = users.find_one({"user_id": user_id}) or {}
    name = user.get("name")
    username = user.get("username")

    if name:
        return f"<a href='tg://user?id={user_id}'>{name}</a>"
    if username:
        return f"@{username}"
    return f"<a href='tg://user?id={user_id}'>User</a>"

#--------IVAN TELL THATS

async def get_name(client, user_id):
    try:
        user = await client.get_users(user_id)
        return user.first_name  # ✅ plain text only
    except:
        return "Unknown User"