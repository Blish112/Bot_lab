from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable, Union

from data.config_reader import admin_id

def _is_admin(user_id) -> bool:
    return user_id == admin_id

class IsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[CallbackQuery, Message],
        data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        user_id = user.id
        
        if _is_admin(user_id):
            return await handler(event, data)
