from aiogram import Router, F
from aiogram.types import Message

from keyboard.common_keyboard import common_keyboard

router = Router()

# Cправочная информация про разделы
@router.message(F.text.lower() == 'справка по разделам 📕')
async def process_help_pressed_press(message: Message) -> None:
    new_text = (
        "Расписание 📗- получить список пар исходя из выбраного дня\n\n"
        "Верификация 🔐- пройти верификацию для получения расписания\n\n"
        "Справка по разделам 📕 - описание и содержание разделов"
    )
    await message.answer(
        text=new_text,
        reply_markup=common_keyboard
    )