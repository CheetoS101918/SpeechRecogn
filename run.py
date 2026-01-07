import asyncio
import logging
from aiogram import Dispatcher, Bot
from handlers import router
from config import Config, load_config

config: Config = load_config('.env')

bot = Bot(token=config.bot.token)
dp = Dispatcher()
dp.message.middleware(MyMiddleware())

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) #, filemode='a', filename='lgg.log'
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop')