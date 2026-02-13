# bot/handlers/__init__.py
# ---------------------------------
# Central handler loader
# Order matters – generic handlers LAST
# ---------------------------------

# ── BASIC / START ─────────────────
from bot.handlers.start import *
from .stats import *
from .broadcast import *
from .feedback import *
# ── USER FEATURES ─────────────────
from bot.handlers.text_menu import *
# ── ADMIN (LAST BEFORE GENERIC) ───
from bot.handlers.admin import *

# ── DO NOT ADD ANY HANDLER AFTER THIS ──
