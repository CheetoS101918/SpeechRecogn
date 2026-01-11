import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from handlers import router
from config import Config, load_config
from fast_whisp_test import processor

config: Config = load_config('.env')

bot = Bot(token=config.bot.token)
dp = Dispatcher()


async def main():
    processor.load_model()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) #, filemode='a', filename='lgg.log'
    try:
        os.mkdir('voices', exist_ok=True)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop')