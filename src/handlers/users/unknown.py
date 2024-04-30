from aiogram import Router
from aiogram.types import Message

from keyboard.common_keyboard import common_keyboard

router = Router()

# Обработка неизветных сообщений
@router.message()
async def unknown_message_hendler(message: Message) -> None:
    await message.answer(
        text='Что-то я не знаю что делать...😵‍💫',
        reply_markup=common_keyboard
    )