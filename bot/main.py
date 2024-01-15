from aiogram import Bot, Dispatcher
from bot.handlers import user, parser_settings
from dotenv import load_dotenv
import os


async def start_bot():
    load_dotenv()
    print(os.getenv('TOKEN'))
    bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')

    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()
    dp.include_routers(
        parser_settings.router,
        user.router,
    )

    await dp.start_polling(bot)
