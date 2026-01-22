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
    logging.basicConfig(
    level=logging.INFO,  # Уровень важности: INFO и выше будут записываться
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Формат сообщения
    handlers=[
        logging.StreamHandler(), # Вывод в консоль
    ]
)
    try:
        if not os.path.isdir('voices'):
            os.mkdir('voices')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop')
    except Exception as e:
        logging.critical("Критическая ошибка при запуске бота!", exc_info=True)  