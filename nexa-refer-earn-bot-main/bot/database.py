from pymongo import MongoClient
from bot.config import MONGO_URI

# ───────────────────────────────────────────────
# MONGODB CONNECTION
# ───────────────────────────────────────────────
mongo = MongoClient(MONGO_URI)

# database name (FIXED – NO AUTO)
db = mongo["nexa"]

print("✅ MongoDB connected successfully")
print("📦 Database in use: nexa")

# ───────────────────────────────────────────────
# COLLECTIONS
# ───────────────────────────────────────────────
users = db["users"]

withdraws = db["withdraws"]

feedbacks = db["feedbacks"]

wallet_logs = db["wallet_logs"]   # ✅ REQUIRED (FIX)

# ───────────────────────────────────────────────
# INDEXES (OPTIONAL BUT GOOD)
# ───────────────────────────────────────────────
users.create_index("user_id", unique=True)
withdraws.create_index("user_id")
wallet_logs.create_index("user_id")
feedbacks.create_index("user_id")