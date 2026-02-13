# bot/utils.py
# -------------------------------------------------
# Common utility functions (FINAL FIXED VERSION)
# -------------------------------------------------

import asyncio
from pyrogram.errors import UserNotParticipant, FloodWait, PeerIdInvalid

from bot.main import app
from bot.config import FORCE_CHANNELS, ADMIN_LOG_GROUP


# ───────────────────────────────────────────────
# FORCE JOIN CHECK (PUBLIC CHANNELS ONLY)
# ───────────────────────────────────────────────
async def is_user_joined(app, user_id: int) -> bool:
    """
    Check whether a user has joined all required PUBLIC channels.
    Private invite links (t.me/+) are skipped.
    """

    for ch in FORCE_CHANNELS:

        # 🔒 Skip private invite links
        if "t.me/+" in ch:
            continue

        channel = (
            ch.replace("https://t.me/", "")
              .replace("http://t.me/", "")
              .replace("@", "")
              .strip()
        )

        try:
            member = await app.get_chat_member(channel, user_id)

            if member.status in ("left", "kicked"):
                return False

        except UserNotParticipant:
            return False

        except FloodWait as e:
            await asyncio.sleep(e.value)
            continue  # retry next channel safely

        except Exception as e:
            print(f"⚠️ Force-join error [{channel}]: {e}")
            return False

    return True


# ───────────────────────────────────────────────
# RESOLVE CHAT (PEER FIX)
# ───────────────────────────────────────────────
async def resolve_chat(chat_id) -> bool:
    """
    Force resolve a chat peer (group/channel/user).
    Prevents PeerIdInvalid errors.
    """
    try:
        await app.get_chat(chat_id)
        return True
    except Exception as e:
        print(f"❌ Resolve chat failed ({chat_id}): {e}")
        return False


# ───────────────────────────────────────────────
# SAFE SEND MESSAGE (GLOBAL)
# ───────────────────────────────────────────────
async def safe_send(chat_id, text: str, **kwargs):
    """
    Safely send a message to any chat.
    Handles PeerIdInvalid + FloodWait correctly.
    """

    try:
        return await app.send_message(chat_id, text, **kwargs)

    except PeerIdInvalid:
        if await resolve_chat(chat_id):
            return await app.send_message(chat_id, text, **kwargs)

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await app.send_message(chat_id, text, **kwargs)

    except Exception as e:
        print(f"⚠️ safe_send failed ({chat_id}): {e}")


# ───────────────────────────────────────────────
# SEND LOG TO ADMIN GROUP (SAFE)
# ───────────────────────────────────────────────
async def send_log(text: str, **kwargs):
    """
    Send log message to admin log group safely.
    """
    if not ADMIN_LOG_GROUP:
        return

    try:
        return await app.send_message(
            ADMIN_LOG_GROUP,
            text,
            disable_web_page_preview=True,
            **kwargs
        )

    except PeerIdInvalid:
        if await resolve_chat(ADMIN_LOG_GROUP):
            return await app.send_message(
                ADMIN_LOG_GROUP,
                text,
                disable_web_page_preview=True,
                **kwargs
            )

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_log(text, **kwargs)

    except Exception as e:
        print(f"⚠️ Log send failed: {e}")


# ───────────────────────────────────────────────
# FORMAT USER NAME
# ───────────────────────────────────────────────
def format_user(user) -> str:
    """
    Return a readable user name.
    """
    if not user:
        return "User"
    if user.username:
        return f"@{user.username}"
    return user.first_name or "User"


# ───────────────────────────────────────────────
# SAFE INTEGER PARSER
# ───────────────────────────────────────────────
def safe_int(value, default=0) -> int:
    """
    Convert value to int safely.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default