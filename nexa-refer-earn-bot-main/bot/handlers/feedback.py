from datetime import datetime, timezone, timedelta

LINE = "━━━━━━━━━━━━━━━━━━"

IST = timezone(timedelta(hours=5, minutes=30))

def ts() -> str:
    """Return formatted India (IST) timestamp."""
    return datetime.now(IST).strftime("%d %b %Y • %I:%M %p")

async def shimmer(msg, base, loops=6, delay=0.25):
    frames = ["✨", "🌒", "🌕", "💫", "🌑"]
    for i in range(loops):
        try:
            await msg.edit_text(f"{frames[i % len(frames)]} {base}")
        except:
            pass
        await asyncio.sleep(delay)
from pyrogram import filters
from pyrogram.errors import FloodWait
import asyncio

from bot.main import app
from bot.keyboards.reply import home_reply_kb
from bot.config import FEEDBACK_IMAGE


# ───────────────────────────────────────────────
# FEEDBACK LOGIC
# ───────────────────────────────────────────────
async def feedback(m):
    msg = await m.reply("📝 Fᴇᴇᴅʙᴀᴄᴋ Pᴀɴᴇʟ Oᴘᴇɴɪɴɢ…")
    await shimmer(msg, "Lᴏᴀᴅɪɴɢ Fᴏʀᴍ")

    try:
        await msg.delete()
    except:
        pass

    await m.reply_photo(
        photo=FEEDBACK_IMAGE,
        caption=(
            "📝 **Fᴇᴇᴅʙᴀᴄᴋ & Sᴜɢɢᴇꜱᴛɪᴏɴꜱ**\n"
            f"{LINE}\n\n"
            "💬 Sʜᴀʀᴇ Yᴏᴜʀ Tʜᴏᴜɢʜᴛꜱ Wɪᴛʜ Uꜱ\n\n"
            "🔗 https://t.me/NexaFeedback\n\n"
            "🙏 Yᴏᴜʀ Fᴇᴇᴅʙᴀᴄᴋ Hᴇʟᴘꜱ Uꜱ Iᴍᴘʀᴏᴠᴇ\n\n"
            f"🕒 {ts()}"
        ),
        reply_markup=home_reply_kb()
    )


# ───────────────────────────────────────────────
# FEEDBACK HANDLER
# ───────────────────────────────────────────────
@app.on_message(filters.private & filters.regex("^📝"))
async def feedback_handler(_, m):
    await feedback(m)