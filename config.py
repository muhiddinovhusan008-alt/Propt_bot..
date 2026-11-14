"""
Konfiguratsiya moduli:
.env faylidan sozlamalarni yuklaydi va tekshiradi.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Loyihaning asosiy katalogi
BASE_DIR = Path(__file__).resolve().parent

# .env faylini yuklash
load_dotenv(BASE_DIR / ".env")

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Administratorlarning Telegram ID raqamlari (Faqat 8235455342)
PRIMARY_ADMIN_ID = 8235455342
admin_ids_raw = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = [PRIMARY_ADMIN_ID]
if admin_ids_raw:
    for item in admin_ids_raw.split(","):
        item = item.strip()
        if item.isdigit():
            val = int(item)
            if val not in ADMIN_IDS:
                ADMIN_IDS.append(val)

# Baza fayli joylashuvi
DB_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "database/bilim_kutubxonasi.db")

# Darslik va kitoblar uchun yuklash papkasi
MEDIA_DIR = BASE_DIR / "media"
BOOKS_DIR = MEDIA_DIR / "books"
BOOKS_DIR.mkdir(parents=True, exist_ok=True)

# Ixtiyoriy proksi
PROXY_URL = os.getenv("PROXY_URL", "").strip() or None

# ==================== WEBHOOK VA VIRTUAL SERVER SOZLAMALARI ====================
# Render muhitini aniqlash va Webhook URL shakllantirish
IS_RENDER = os.getenv("RENDER", "").lower() in ("true", "1") or bool(os.getenv("RENDER_EXTERNAL_HOSTNAME")) or bool(os.getenv("RENDER_SERVICE_ID"))
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "").strip()

if not RENDER_EXTERNAL_URL and RENDER_EXTERNAL_HOSTNAME:
    RENDER_EXTERNAL_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"

if not RENDER_EXTERNAL_URL and IS_RENDER:
    RENDER_EXTERNAL_URL = "https://propt-bot-2.onrender.com"

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip() or RENDER_EXTERNAL_URL

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook").strip()
if not WEBHOOK_PATH.startswith("/"):
    WEBHOOK_PATH = f"/{WEBHOOK_PATH}"

# Telegram Webhook xavfsizligi uchun maxfiy kalit (Secret Token)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "bilim_kutubxonasi_secret_token_key").strip()

# Render Web Service tinglaydigan port va xost
PORT = int(os.getenv("PORT", 10000))
HOST = os.getenv("HOST", "0.0.0.0")
