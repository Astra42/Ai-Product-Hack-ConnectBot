import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommandScopeDefault
from handlers import router
from keyboards import navigation_kb

with open("bot_token.txt", 'r') as f:
    TOKEN = f.read()
    print(TOKEN)

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')


async def main():
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    await bot.set_my_commands(navigation_kb, BotCommandScopeDefault())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disabled")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/