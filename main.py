"""
«BILIM KUTUBXONASI» Telegram botining asosiy ishga tushiruvchi fayli (entrypoint).
Render Free Web Service uchun Webhook va lokal sinovlar uchun Polling rejimlarini qo'llab-quvvatlaydi.
"""

import sys
import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import (
    BOT_TOKEN,
    ADMIN_IDS,
    PROXY_URL,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBHOOK_SECRET,
    PORT,
    HOST
)
from database import init_db
from handlers import setup_routers
from middlewares import InstagramSubscriptionMiddleware

# Logging konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("BilimKutubxonasi")


async def health_check(request: web.Request) -> web.Response:
    """Render Web Service va monitoring tizimlari uchun Health Check endpointi."""
    return web.Response(
        text="Bilim Kutubxonasi Telegram Bot is active and healthy! 🚀",
        status=200,
        content_type="text/plain"
    )


async def on_startup(bot: Bot):
    """Bot ishga tushganda bajariladigan amallar."""
    logger.info("Ma'lumotlar bazasi initsializatsiya qilinmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")

    # Webhook sozlash (agar WEBHOOK_URL mavjud bo'lsa)
    if WEBHOOK_URL:
        full_webhook_url = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
        logger.info(f"Webhook o'rnatilmoqda: {full_webhook_url}")
        try:
            await bot.set_webhook(
                url=full_webhook_url,
                secret_token=WEBHOOK_SECRET,
                drop_pending_updates=True
            )
            logger.info("Webhook muvaffaqiyatli o'rnatildi!")
        except Exception as e:
            logger.error(f"Webhook o'rnatishda xatolik: {e}")

    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot muvaffaqiyatli ulandi: @{bot_info.username} ({bot_info.first_name})")

        # Adminlarga xabarnoma yuborish
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"🚀 <b>«Bilim Kutubxonasi» boti ishga tushirildi!</b>\n"
                         f"🤖 Bot: @{bot_info.username}\n"
                         f"🌐 Rejim: <b>{'Webhook (Render Web Service)' if WEBHOOK_URL else 'Polling'}</b>",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logger.warning(f"Adminga ({admin_id}) xabar yetkazilmadi: {e}")
    except Exception as e:
        logger.warning(f"Bot info olishda ogohlantirish: {e}")


async def on_shutdown(bot: Bot):
    """Bot to'xtatilganda bajariladigan amallar."""
    logger.info("Bot to'xtatilmoqda...")
    if WEBHOOK_URL:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook o'chirildi.")
        except Exception as e:
            logger.warning(f"Webhook o'chirishda xatolik: {e}")

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="⚠️ <b>«Bilim Kutubxonasi» boti to'xtatildi!</b>",
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass

    await bot.session.close()


def create_bot_and_dispatcher():
    """Bot va Dispatcher obyektlarini yaratish."""
    session = None
    if PROXY_URL:
        logger.info(f"Proksi orqali ulanmoqda: {PROXY_URL}")
        session = AiohttpSession(proxy=PROXY_URL)

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Instagram obunasini tekshirish middleware'larini ulash
    dp.message.middleware(InstagramSubscriptionMiddleware())
    dp.callback_query.middleware(InstagramSubscriptionMiddleware())

    dp.include_router(setup_routers())

    # Startup va Shutdown ro'yxatdan o'tkazish
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return bot, dp


async def on_polling_startup(app: web.Application):
    """Polling rejimida ishga tushganda bazani ishga tushirish va polling taskini yaratish."""
    bot: Bot = app["bot"]
    dp: Dispatcher = app["dp"]

    logger.info("Ma'lumotlar bazasi initsializatsiya qilinmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Eski webhooklar tozalandi.")
    except Exception as e:
        logger.warning(f"Webhook tozalashda ogohlantirish: {e}")

    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot muvaffaqiyatli ulandi (Polling rejim): @{bot_info.username} ({bot_info.first_name})")
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"🚀 <b>«Bilim Kutubxonasi» boti ishga tushirildi!</b>\n"
                         f"🤖 Bot: @{bot_info.username}\n"
                         f"🌐 Rejim: <b>Polling + Render Web Server (Port {PORT})</b>",
                    parse_mode=ParseMode.HTML
                )
            except Exception:
                pass
    except Exception as e:
        logger.warning(f"Bot ma'lumotlarini olishda ogohlantirish: {e}")

    # Pollingni fon vazifasi sifatida ishga tushirish
    app["polling_task"] = asyncio.create_task(dp.start_polling(bot))


async def on_polling_shutdown(app: web.Application):
    """Polling fon vazifasini va sessiyani to'xtatish."""
    logger.info("Bot (Polling) to'xtatilmoqda...")
    task = app.get("polling_task")
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    bot: Bot = app.get("bot")
    if bot:
        await bot.session.close()


def main():
    """Asosiy ishga tushirish funksiyasi."""
    if not BOT_TOKEN or "YOUR_" in BOT_TOKEN:
        logger.error(
            "\n" + "=" * 60 + "\n"
            "XATOLIK: .env faylida yoki muhit o'zgaruvchilarida BOT_TOKEN ko'rsatilmagan!\n"
            "Iltimos, BOT_TOKEN ni kiriting.\n"
            "=" * 60
        )
        sys.exit(1)

    bot, dp = create_bot_and_dispatcher()

    app = web.Application()
    app["bot"] = bot
    app["dp"] = dp

    # Health check yo'nalishlari (Render va monitoring tizimlari uchun)
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    if WEBHOOK_URL:
        # ==================== RENDER FREE WEB SERVICE (WEBHOOK REJIMI) ====================
        logger.info(f"Render Free Web Service Webhook rejimida ishga tushirilmoqda. URL: {WEBHOOK_URL}, Port: {PORT}")

        # Telegram yangilanishlarini qabul qiluvchi Webhook handler
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        # aiogram ilovasini aiohttp bilan integratsiyalash
        setup_application(app, dp, bot=bot)
    else:
        # ==================== GIBRID REJIM (WEB SERVER + POLLING) ====================
        # Renderda port yopilib qolmasligi va healthcheck yiqilmasligi uchun veb-server va polling birga ishlaydi
        logger.info(f"WEBHOOK_URL aniqlanmadi. Veb-server va Polling gibrid rejimida ishga tushmoqda. Port: {PORT}")
        app.on_startup.append(on_polling_startup)
        app.on_shutdown.append(on_polling_shutdown)

    # Har qanday holatda Render kutgan PORT da veb-serverni ishga tushirish
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
