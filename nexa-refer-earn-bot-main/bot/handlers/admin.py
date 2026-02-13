from pyrogram import filters
from bot.main import app
from bot.database import withdraws, users
from bot.config import ADMIN_IDS

@app.on_callback_query(filters.regex("^wd_"))
async def admin_withdraw(_, q):
    if q.from_user.id not in ADMIN_IDS:
        return

    _, action, wid = q.data.split("_")
    wd = withdraws.find_one({"_id": wid})

    if not wd or wd["status"] != "pending":
        return

    if action == "approve":
        withdraws.update_one({"_id": wd["_id"]},{"$set":{"status":"approved"}})
        await app.send_message(wd["user_id"],"✅ **Wɪᴛʜᴅʀᴀᴡ Aᴘᴘʀᴏᴠᴇᴅ**")
        await q.message.edit_text("✅ Approved")

    else:
        withdraws.update_one({"_id": wd["_id"]},{"$set":{"status":"rejected"}})
        users.update_one({"user_id":wd["user_id"]},{"$inc":{"stars":wd["amount"]}})
        await app.send_message(wd["user_id"],"❌ **Wɪᴛʜᴅʀᴀᴡ Rᴇᴊᴇᴄᴛᴇᴅ**")
        await q.message.edit_text("❌ Rejected")