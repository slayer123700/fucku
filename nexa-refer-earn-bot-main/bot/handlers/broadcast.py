from pyrogram import filters
from pyrogram.errors import FloodWait
import asyncio

from bot.main import app
from bot.database import users
from bot.config import ADMIN_IDS


LINE = "━━━━━━━━━━━━━━━━━━"


# ───────────── /broadcast (ADMIN ONLY) ─────────────
@app.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler(_, m):
    if m.from_user.id not in ADMIN_IDS:
        return await m.reply("❌ **Aᴄᴄᴇss Dᴇɴɪᴇᴅ**")

    if len(m.command) < 2:
        return await m.reply(
            "📢 **Bʀᴏᴀᴅᴄᴀsᴛ Uꜱᴀɢᴇ**\n\n"
            "`/broadcast Your message here`"
        )

    text = m.text.split(None, 1)[1]

    sent = failed = 0
    status = await m.reply("📢 **Bʀᴏᴀᴅᴄᴀsᴛ Sᴛᴀʀᴛᴇᴅ…**")

    for u in users.find({}, {"user_id": 1}):
        try:
            await app.send_message(u["user_id"], text)
            sent += 1
            await status.edit_text(
                f"📢 **Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ…**\n\n"
                f"📤 Sᴇɴᴛ: `{sent}`\n"
                f"❌ Fᴀɪʟᴇᴅ: `{failed}`"
            )
            await asyncio.sleep(0.04)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except:
            failed += 1

    await status.edit_text(
        f"✅ **Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇ**\n{LINE}\n\n"
        f"📤 Sᴇɴᴛ: `{sent}`\n"
        f"❌ Fᴀɪʟᴇᴅ: `{failed}`"
    )