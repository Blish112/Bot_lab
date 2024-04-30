from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from db.querys.user_query import get_user_is_accept, get_user_group

async def _is_accept(user) -> bool:
    return await get_user_is_accept(user) 

async def _have_group(user) -> bool:
    group = await get_user_group(user)
    return group is not None

class UserAcceptMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        user_id = user.id
        
        if await _is_accept(user_id):
            return await handler(event, data)
        
        if await _have_group(user_id):
            await event.answer(
                "Вы не закончили процесс верификацию!",
                show_alert=True
            )
        else:
            await event.answer(
                "Вы еще не прошли верифекацию!",
                show_alert=True
            )
