from pyrogram import filters
import asyncio

from bot.main import app
from bot.database import users
from bot.config import ADMIN_IDS


LINE = "━━━━━━━━━━━━━━━━━━"


async def animated_counter(msg, title, value):
    step = max(1, value // 20)
    cur = 0
    while cur < value:
        cur += step
        if cur > value:
            cur = value
        try:
            await msg.edit_text(
                f"📊 **{title}**\n{LINE}\n\n`{cur}`"
            )
        except:
            pass
        await asyncio.sleep(0.08)


# ───────────── /stats (ADMIN ONLY) ─────────────
@app.on_message(filters.private & filters.command("stats"))
async def stats_handler(_, m):
    if m.from_user.id not in ADMIN_IDS:
        return await m.reply("❌ **Aᴄᴄᴇss Dᴇɴɪᴇᴅ**")

    msg = await m.reply("📊 **Cᴀʟᴄᴜʟᴀᴛɪɴɢ…**")

    total_users = users.count_documents({})
    total_stars = sum(u.get("stars", 0) for u in users.find())

    await animated_counter(msg, "Uꜱᴇʀs", total_users)
    await animated_counter(msg, "Tᴏᴛᴀʟ Sᴛᴀʀs", total_stars)

    await msg.edit_text(
        f"📊 **Bᴏᴛ Sᴛᴀᴛs**\n{LINE}\n\n"
        f"👥 **Uꜱᴇʀs:** `{total_users}`\n"
        f"⭐ **Sᴛᴀʀs:** `{total_stars}`"
    )