from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.fsm.storage.redis import RedisStorage
from typing import Callable, Dict, Any, Awaitable, Union

class AntiSpam(BaseMiddleware):
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        user_id = f'user{user.id}'
        
        check_user = await self.storage.redis.get(name=user_id)
        
        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user_id, value=0, ex=5)
                return await event.answer('Мы обнаружили подозртельную активность. Подождите пару секунд.')
            return
        await self.storage.redis.set(name=user_id, value=1, ex=5)
        return await handler(event, data)
