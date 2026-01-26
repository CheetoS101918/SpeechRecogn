from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from config import Config, load_config
import logging


logger = logging.getLogger(__name__)
config: Config = load_config('.env')
adm_id: int = config.bot.admin_ids 


class Notifier(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user = data.get("event_from_user")
        bot = data['bot']
        
        if user and user.id == adm_id:
            return await handler(event, data)

        if user and (not user.is_bot):
            if user.id != adm_id:
                try:
                    await bot.send_message(
                        adm_id,
                        f"🚀 Новый пользователь!\n\n"
                        f"Имя: {user.full_name}\n"
                        f"ID: `{user.id}`\n"
                        f"Username: @{user.username or 'отсутствует'}"
                    )
                except Exception as e:
                    logger.error(f'error notifying admin about a new user: {e}')

        result = await handler(event, data)
        return result