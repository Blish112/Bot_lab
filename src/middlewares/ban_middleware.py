from aiogram import BaseMiddleware
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery, InlineQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable, Union

from db.querys.user_query import get_user_is_baned

async def _is_baned(user) -> bool:
    return await get_user_is_baned(user)

class UserBannedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery, InlineQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        user_id = user.id
        
        if not await _is_baned(user_id):
            return await handler(event, data)
        
        await event.answer(
            '<b> Ваш аккаунт заблокирован!</b>',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            parse_mode=ParseMode.HTML,
            show_alert=True
        )
