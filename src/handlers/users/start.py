import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from data.config_reader import admin_id
from keyboard.start_keyboard import keyboard_start_help

from db.model import User
from db.querys.user_query import (
    get_user, 
    insert_user, 
    upd_user_data_using,
    get_user_first_name,
    upd_user_first_name,
    get_user_fullname,
    upd_user_fullname
)


router = Router()

# Начало работы. Команда старт. Начальная страница
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await check_user(message)
    
    bot_name = "Schedule_SURGU_Bot"
    hello_text = (
        f"Привет! Меня зовут {hbold(bot_name)}!\n"
        f"Я - бот-помощник, который всегда в курсе твоего расписания📅\n\n"
        f"Перед началом работы обязательно пройди верификацию🚨\n\n"
        f"Дальнейшие инструкции будут в соответвующем разделе😉"
    )
    
    # TODO: сделать админку
    await message.answer(
        text=hello_text,
        reply_markup=keyboard_start_help
    )

# Обработка callback_query при нажатии кнопки возврата на нач. стр. 
@router.callback_query(F.data == 'back_pressed')
async def process_back_press(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await command_start_handler(callback.message)


# check user's data in DB
async def check_user(message: Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_fullname = message.from_user.username
    
    # Create new user and add to db
    if await get_user(user_id) is None:
        user = User(
            tg_id=message.from_user.id,
            fullname=message.from_user.username,
            first_name=message.from_user.first_name,
        )
        await insert_user(user)  
    
    # Upd first_name
    if await get_user_first_name(user_id=user_id) != user_first_name:
        await upd_user_first_name(
            user_id=user_id, 
            first_name=user_first_name
        )
    
    # Upd fullname
    if await get_user_fullname(user_id=user_id) != user_fullname:
        await upd_user_fullname(
            user_id=user_id, 
            fullname=user_fullname
        )
        
    # Upd data using
    await upd_user_data_using(
        user_id=message.from_user.id,
        time=datetime.datetime.now(datetime.timezone.utc)
    )
        