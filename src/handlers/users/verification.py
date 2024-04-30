from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.config_reader import code_words, list_code_word
from db.querys.group_query import get_group
from db.querys.user_query import (
    get_user_try_to_acept, 
    upd_user_try_to_acept, 
    get_user_group,
    upd_user_group,
    upd_user_is_accept,
    upd_user_is_baned
)

from keyboard.common_keyboard import common_keyboard
from keyboard.verification_keyboard import(
    keyboard_verification_restart,
    keyboard_verification, 
    keyboard_start
)

# Класс формы для вкл/выкл обработки определенных сообщений
class Form(StatesGroup):
    number_of_group = State()
    codes_word = State()
    start_is_pressed = State()

router = Router()

# Блок верификации
@router.message(F.text.lower() == 'верификация 🔐')
async def command_verificator_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start_is_pressed)
    
    text_verif_start = (
        "Вам предстоит пройти верификацию.\n\n"
        "От вас потребуется ввести номер группы и кодовое слово 🤫\n"
    )
    
    text_verif_return = (
        "С возвращением.🔥\n\n"
        "Вам осталось только ввести кодовое слово 🤫\n"
    )
    
    user_id = message.from_user.id
    user_group_id = await get_user_group(user_id)
    
    if user_group_id is not None:
        await state.update_data(number_of_group=str(user_group_id.id))
        
        await message.answer(
            text=text_verif_return, 
            reply_markup=keyboard_verification_restart
        )
    else:
        await message.answer(
            text=text_verif_start, 
            reply_markup=keyboard_verification
        )

# Обработка случая, если не нажата кнопка старт
@router.message(Form.start_is_pressed)
async def start_is_not_pressed_hendler(message: Message, state: FSMContext) -> None:
    await message.answer(
        text='<b>Перед началом ввода сообщений на кнопку Старт ⭐️</b>\n\n',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard_verification
    )

# Обработка номера группы, если введен нужный формат
@router.message(Form.number_of_group, F.text.casefold().regexp(r'^\d{3}-\d{2}[мМ]'))
async def regexp_grop_num_hendler(message: Message, state: FSMContext) -> None:
    grouop = await get_group(message.text) 
    if grouop is not None:
        await state.update_data(number_of_group=str(grouop.id))
        await state.set_state(Form.codes_word)
        
        await upd_user_group(message.from_user.id, message.text)
        
        await message.answer(
            text='Отлично!\nТеперь введите кодовое слово.',
            reply_markup=keyboard_start
        )
    else:
        await state.clear()
        await message.answer(
            text=f'Такая группа не найдена 😢',
            reply_markup=common_keyboard
        )
    
# Обработка неправельного ввода номера группы 
@router.message(Form.number_of_group)
async def regexp_grop_num(message: Message) -> None:
    await message.reply(
        text=f'Неверный формат ввода. Попробуйте заново',
        reply_markup=common_keyboard
    )

# Обработка кодового слова, если такое слова есть в списке кл. слов 
@router.message(Form.codes_word, F.text.in_(list_code_word))
async def code_word_in_list_hendler(message: Message, state: FSMContext) -> None:
    data = await state.update_data(codes_word=message.text)
    
    user_id = message.from_user.id
    user_try_accept = await get_user_try_to_acept(user_id)
    user_try_accept -= 1
    await upd_user_try_to_acept(user_id, user_try_accept)
    
    if (message.text == code_words[data['number_of_group']]):
        await upd_user_is_accept(user_id, True)
        await state.clear()
        await message.answer(
            text='Верификация пройдена успешно!',
            reply_markup=common_keyboard
        )
    elif user_try_accept > 0:
        await message.reply(
            text=(
                'Неверно! Это кодовое слово не подходит для данной группы.\n'
                f'Попробуйте заново.\n\n'
                f'Количество оставшихся попыток: <b>{user_try_accept}</b>'
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=common_keyboard
        )
    else:
        await state.clear()
        await upd_user_try_to_acept(user_id, user_try_accept)
        await upd_user_is_baned(user_id, True)
        await message.answer(
            '<b> Ваш аккаунт заблокирован!</b>',
            show_alert=True
        )


# Обработка неправельного ввода ключевого слова 
@router.message(Form.codes_word)
async def code_word_out_of_list_hendler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_try_accept = await get_user_try_to_acept(user_id)
    user_try_accept -= 1
    await upd_user_try_to_acept(user_id, user_try_accept)
    
    if user_try_accept > 0:
        await message.reply(
            text=(
                'Неверно! Это кодовое слово не подходит для данной группы\n'
                f'Попробуйте заново.\n\n'
                f'Количество оставшихся попыток: <b>{user_try_accept}</b>'
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=common_keyboard
        )
    else:
        await state.clear()
        await upd_user_try_to_acept(user_id, user_try_accept)
        await upd_user_is_baned(user_id, True)
        await message.answer(
            '<b> Ваш аккаунт заблокирован!</b>',
            show_alert=True
        )

# Кнопка старт
@router.callback_query(Form.start_is_pressed, F.data == 'start_pressed')
async def process_start_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(start_is_pressed='1')
    await state.set_state(Form.number_of_group)
    
    if callback.message.text != 'Пожалуйста, ведите номер группы в формате 601-21м':
        await callback.message.edit_text(
            text='Пожалуйста, ведите номер группы в формате *601-21м*',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard_start
        )
    await callback.answer()
    
# Кнопка изменить номер группы
@router.callback_query(Form.start_is_pressed, F.data == 'restart_pressed')
async def process_start_press(callback: CallbackQuery, state: FSMContext):
    await upd_user_try_to_acept(callback.from_user.id, 3)
    await upd_user_is_accept(callback.from_user.id, False)
    
    await state.update_data(start_is_pressed='1')
    await state.set_state(Form.number_of_group)
    
    if callback.message.text != 'Пожалуйста, ведите номер группы в формате 601-21м':
        await callback.message.edit_text(
            text='Пожалуйста, ведите номер группы в формате *601-21м*',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard_start
        )
    await callback.answer()
    
# Кнопка продолжить
@router.callback_query(Form.start_is_pressed, F.data == 'continue_pressed')
async def process_start_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(start_is_pressed='1')
    await state.set_state(Form.codes_word)
    
    if callback.message.text != 'Отлично!\nТеперь введите кодовое слово':
        await callback.message.edit_text(
            text='Отлично!\nТеперь введите кодовое слово',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard_start
        )
    await callback.answer()

# Кнопка старт-назад
@router.callback_query(F.data == 'start_back_pressed')
async def process_start_back_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await command_verificator_handler(callback.message, state)
