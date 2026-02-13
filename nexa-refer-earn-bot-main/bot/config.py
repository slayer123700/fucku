import os


# ───────────────────────────────────────────────
# TELEGRAM API (REQUIRED)
# ───────────────────────────────────────────────
API_ID = int(os.getenv("API_ID", "26249286"))
API_HASH = os.getenv("API_HASH", "4e3bf0b014fda4ac752e8f4ab854279b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8571848657:AAE9KdCNJsBbnTayMJvhJG6Ijzw1t2XuSd8")

BOT_USERNAME = os.getenv("BOT_USERNAME", "Earntgidbot")

DATABASE_NAME = "test"

# ───────────────────────────────────────────────
# MONGODB (REQUIRED)
# ───────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lollolopp0900:slayersan@cluster0.mge1ngz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


FEEDBACK_IMAGE = "https://files.catbox.moe/45m3vs.jpg"

# ───────────────────────────────────────────────
# ADMINS (SPACE SEPARATED IDS)
# Example: ADMINS="123456789 987654321"
# ───────────────────────────────────────────────
ADMIN_IDS = list(
    map(int, os.getenv("ADMINS", "").split())
) if os.getenv("ADMINS") else []


# Admin log group (private, must start with -100)
ADMIN_LOG_GROUP = int(os.environ.get("ADMIN_LOG_GROUP", "0"))

# Public group username OR private group ID
ADMIN_LOG_GROUP = "@abrakadabraIVANKICHUT"

LEAVE_DEDUCT_STARS = 5


# ───────────────────────────────────────────────
# SUPPORT
# ───────────────────────────────────────────────
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "NexaSupports")


# ───────────────────────────────────────────────
# FORCE JOIN CHANNELS
# SPACE separated usernames / invite links
# Example env:
# FORCE_CHANNELS="@NexaCoders https://t.me/+abc123"
# ───────────────────────────────────────────────
FORCE_CHANNELS = os.getenv(
    "FORCE_CHANNELS",
    "https://t.me/NexaCoders https://t.me/+QmQyNkMs0IQyY2U1 https://t.me/VeronCoders https://t.me/+nNGDcwvjTTY5NGE1 https://t.me/+RXlA2uR_9rdkZjQ1 https://t.me/+wgHJv9cPPNhmY2M1 https://t.me/+gCfYMfN1TQ41ODVh https://t.me/+13LfdFrlHlNhYmY9"
).split()


# ───────────────────────────────────────────────
# BONUSES
# ───────────────────────────────────────────────
JOIN_BONUS = int(os.getenv("JOIN_BONUS", "1"))

# Daily streak rewards
STREAK_REWARDS = [
    1,  # Day 1
    1,  # Day 2
    1,  # Day 3
    1,  # Day 4
    1,  # Day 5
    1,  # Day 6
    1   # Day 7+
]

# Extra milestone bonus
STREAK_MILESTONES = {
    7: 10,
    14: 20,
    30: 50
}


# ───────────────────────────────────────────────
# WITHDRAW SETTINGS
# ───────────────────────────────────────────────
WITHDRAW_AMOUNTS = [15, 25, 50, 75, 100, 300, 400]


# ───────────────────────────────────────────────
# ASSETS (URL or local path)
# ───────────────────────────────────────────────
START_IMAGE = os.getenv(
    "START_IMAGE",
    "https://files.catbox.moe/m9c28g.jpg"
)

MUST_JOIN_IMAGE = os.getenv(
    "MUST_JOIN_IMAGE",
    "https://files.catbox.moe/brqx6l.jpg"
)
