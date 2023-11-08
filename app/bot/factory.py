from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.settings import settings



async def on_startup(bot: Bot) -> None:

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        settings.WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=settings.TELEGRAM_SECRET.get_secret_value()
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()


    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.update.middleware(ThrottlingMiddleware())

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)