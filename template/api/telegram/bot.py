import asyncio
import logging
import threading
from contextlib import asynccontextmanager
import redis.asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from django.conf import settings

from template.api.telegram.middleware import CheckUserMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def bot_lifespan():
    # All project imports should be done there
    from template.api.telegram.routers import router as main_router

    r = redis.asyncio.from_url(settings.FSM_STORAGE_URL)
    storage = RedisStorage(r, key_builder=DefaultKeyBuilder(with_destiny=True))

    bot = Bot(settings.TELEGRAM_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        main_router,
    )

    dp.message.middleware(CheckUserMiddleware())
    dp.callback_query.middleware(CheckUserMiddleware())
    logger.warning("Initializing bot...")

    async def start_bot():
        logger.warning("Starting polling...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            handle_signals=False,
        )

    if settings.BOT_USE_POLLING:
        threading.Thread(daemon=True, target=asyncio.run, args=(start_bot(),)).start()
        yield {}
    else:
        logger.warning("Setting up webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(settings.WEBHOOK_URL)
        yield {
            "dp": dp,
            "bot": bot,
        }

    await bot.close()
