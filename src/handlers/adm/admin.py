from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.querys.group_query import insert_group, get_group, del_group
from db.model import Group

from middlewares.admin_middleware import IsAdmin

from keyboard.common_keyboard import common_keyboard
from keyboard.admin_keyboard import(
    keyboard_start_add,
    keyboard_start_del
)

router = Router()
router.message.middleware(IsAdmin())
router.callback_query.middleware(IsAdmin())

class Form(StatesGroup):
    add_number_of_group = State()
    add_start_is_pressed = State()
    del_number_of_group = State()
    del_start_is_pressed = State()
    
@router.message(Command("add_group"))
async def add_group_hendler(message: Message, state: FSMContext):
    await state.set_state(Form.add_start_is_pressed)
    await message.answer(
        text="Здарова отец! Добавим новенького?",
        reply_markup=keyboard_start_add
    )
    
@router.message(Form.add_number_of_group, F.text.casefold().regexp(r'^\d{3}-\d{2}[мМ]'))
async def regexp_grop_num_hendler(message: Message, state: FSMContext) -> None:
    await state.update_data(add_number_of_group=message.text)
    await state.clear()
    
    number_of_group: Group = Group(
        name_group=message.text
    )
    if await get_group(message.text) is not None:
        await insert_group(number_of_group)
    
    await message.answer(
        text="Группа успешно добавлена!",
        reply_markup=keyboard_start_add
    )
    
# Обработка неправельного ввода номера группы 
@router.message(Form.add_number_of_group)
async def regexp_grop_num(message: Message) -> None:
    await message.reply(
        text=f'Неверный формат ввода. Попробуйте заново',
        reply_markup=common_keyboard
    )
    
# Кнопка старт
@router.callback_query(Form.add_start_is_pressed, F.data == 'add_start_pressed')
async def process_start_press(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(start_is_pressed='1')
    await state.set_state(Form.add_number_of_group)
    
    if callback.message.text != 'Пожалуйста, ведите номер группы в формате 601-21м':
        await callback.message.edit_text(
            text='Пожалуйста, ведите номер группы в формате *601-21м*',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard_start_add
        )
    await callback.answer()
    

@router.message(Command("del_group"))
async def del_group_hendler(message: Message, state: FSMContext):
    await state.set_state(Form.del_start_is_pressed)
    await message.answer(
        text="Здарова отец! Пора кого-то убрать ...",
        reply_markup=keyboard_start_del
    )
    
@router.message(Form.del_number_of_group, F.text.casefold().regexp(r'^\d{3}-\d{2}[мМ]'))
async def regexp_grop_num_hendler(message: Message, state: FSMContext) -> None:
    await state.update_data(del_number_of_group=message.text)
    await state.clear()
    
    
    await del_group(message.text)
    
    await message.answer(
        text="Группа успешно удалена!",
        reply_markup=keyboard_start_del
    )
    
# Обработка неправельного ввода номера группы 
@router.message(Form.del_number_of_group)
async def regexp_grop_num(message: Message) -> None:
    await message.reply(
        text=f'Неверный формат ввода. Попробуйте заново',
        reply_markup=common_keyboard
    )
    
# Кнопка старт
@router.callback_query(Form.del_start_is_pressed, F.data == 'del_start_pressed')
async def process_start_press(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(start_is_pressed='1')
    await state.set_state(Form.del_number_of_group)
    
    if callback.message.text != 'Пожалуйста, ведите номер группы в формате 601-21м':
        await callback.message.edit_text(
            text='Пожалуйста, ведите номер группы в формате *601-21м*',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard_start_del
        )
    await callback.answer()
    