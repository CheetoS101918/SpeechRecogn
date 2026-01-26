import asyncio
import logging
import os
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from concurrent.futures import ThreadPoolExecutor
from fast_whisp_test import processor
from aiogram import F, Router


MAX_VOICE_DURATION = 60
pool = ThreadPoolExecutor(max_workers=1) 
router = Router()

logger = logging.getLogger(__name__) # __name__ автоматически даст имя модуля: 'fast_whisp_test'


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Я умею распознавать речь в гс! Просто перешли сюда нужное тебе гс и ответь на него командой /run!',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('run'))
async def transcribe(message: Message):

    logger.info(f'recieved message from {message.from_user.id}')

    if not message.reply_to_message:
        await message.answer('нужно именно ОТВЕТИТЬ на гс командой /run чтобы я понял, какое конкретно гс тебе нужно')
        return

    voice = message.reply_to_message.voice

    # if voice.duration > MAX_VOICE_DURATION:
    #     await message.reply_to_message.reply(f'гс должно быть не более {MAX_VOICE_DURATION} сек')
    
    if not voice:
        await message.answer('нужно ответить именно на ГС')
        return

    file_id = voice.file_id
    file = await message.bot.get_file(file_id)

    try:
        await message.bot.download_file(
            file.file_path,
            destination=f'voices/{file_id}.ogg'
        )
        logger.info(f'file {file_id} successfully downloaded')
    except Exception as e:
        logging.error(f'AN ERROR OCCURED WHILE DOWNLOADING file {file_id}: {e}')

    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(pool, processor.transcribe, file_id)
        await message.reply_to_message.reply("".join(result))
        os.remove(f'voices/{file_id}.ogg')
    except Exception as e:
        logger.error(f'AN ERROR OCCURED WHILE TRANCRIBITION: {e}')
        await message.reply_to_message.reply('ой, что-то пошло не так(\nприносим извинения за временные неудобства\nповторите попытку чуть позже')


