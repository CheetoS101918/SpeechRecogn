from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ChatAction


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Я умею распознавать речь в гс! Просто ответь на нужное тебе гс командой /run!'
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

    file = await message.bot.get_file(voice.file_id)

    await message.bot.download_file(
        file.file_path,
        destination='voices/input.ogg'
    )