import asyncio
import os
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from concurrent.futures import ThreadPoolExecutor
from fast_whisp_test import processor
from aiogram import F, Router


pool = ThreadPoolExecutor(max_workers=1) 

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Я умею распознавать речь в гс! Просто ответь на нужное тебе гс командой /run!',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('run'))
async def transribe(message: Message):

    if not message.reply_to_message:
        await message.answer('нужно именно ОТВЕТИТЬ на гс командой /run чтобы я понял, какое конкретно гс тебе нужно')
        return

    voice = message.reply_to_message.voice
    
    if not voice:
        await message.answer('нужно ответить именно на ГС')
        return

    file_id = voice.file_id
    file = await message.bot.get_file(file_id)

    await message.bot.download_file(
        file.file_path,
        destination=f'voices/{file_id}.ogg'
    )

    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(pool, processor.transcribe, file_id)

    await message.reply_to_message.reply("".join(result))

#    os.remove(f'voices/{file_id}')



