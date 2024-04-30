from datetime import datetime

from aiogram import Router, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from db.querys.numerator_query import get_numerator
from db.querys.classes_query import get_classes_chec, get_classes_znam
from db.querys.user_query import get_user
from db.querys.schedule_query import get_schedule_by_id
from db.querys.subject_query import get_subject
from middlewares.accept_middleware import UserAcceptMiddleware
from keyboard.shcedule_keyboard import get_keyboard_fab, WeekdayCallbackFactory

router = Router()
router.message.middleware(UserAcceptMiddleware())

# Блок расписание
@router.message(F.text.lower() == 'расписание 📗')
async def command_give_shedule(message: Message) -> None:
    await message.answer(
        text='Выберите день:',
        reply_markup=get_keyboard_fab()
    )

# Обработка кнопок
@router.callback_query(WeekdayCallbackFactory.filter())
async def callbacks_weekday_pressed(callback: CallbackQuery, callback_data: WeekdayCallbackFactory):
    text: str
    day: int
    
    if callback_data.weekday == 'Сегодня':
        text = 'Сегодня у вас такие пары:\n\n'
        now = datetime.now()
        day = datetime.isoweekday(now)
        
    if callback_data.weekday == 'Завтра':
        text = 'Завтра у вас такие пары:\n\n'
        now = datetime.now()
        now = datetime.isoweekday(now)
        day = now + (1 if now < 6 else 0)
    
    if callback_data.num_weekday is not None:
        text = 'Пары' + ' во ' if callback_data.weekday == 'Вторник' else ' в '
        text += f'{callback_data.weekday}:\n\n'
        day = callback_data.num_weekday
    
    text = await text_to_message(day, text, callback)
    
    try:
        await callback.message.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=callback.message.reply_markup
        )
    except TelegramBadRequest:
        await callback.answer(
            text='Вы уже нажли на эту кнопку',
            show_alert=True
        )
    finally:
        await callback.answer()
    
# Кнопка числитель/знаменатель
@router.callback_query(F.data == 'chis_znam_pressed')
async def process_chis_znam_press(callback: CallbackQuery):
    numerator = await get_numerator(id_numerator=1)
    text = 'Числитель' if numerator.what_is_now else 'Знаменатель'
            
    try:
        await callback.message.edit_text(
            text=f'Сейчас <b>{text}</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=callback.message.reply_markup
        )
    except TelegramBadRequest:
        await callback.answer(
            text='Вы уже нажли на эту кнопку',
            show_alert=True
        )
    finally:
        await callback.answer()

# Работа с БД
async def text_to_message(date, text: str, callback: CallbackQuery) -> str:
    user = await get_user(user_id=callback.from_user.id)
    classes_for_ches = await get_classes_chec(weekday=date, num_group=user.id_group)
    classes_for_znam = await get_classes_znam(weekday=date, num_group=user.id_group)
    
    if classes_for_ches is not None:
        text += '<b>Числитель:</b>'
        for ches in classes_for_ches:
            subject = await get_subject(ches.id_subject)
            shedule = await get_schedule_by_id(id_schedule=ches.id_schedule)
        
            text += f'\n{ches.class_number}. <u>{subject.name}</u>\n'
            text += f'    \nНачало пары: {str(shedule.start_time)}\nКонец пары:    {str(shedule.end_time)}\n'
            text += f'    \nСсылка на Moodle: \n{subject.moodle_link}\n'
            if subject.second_link is not None:
                text += f'    \nЗапасная ссылка: {subject.second_link}\n'
    
    if classes_for_ches is not None:     
        text += '\n<b>Знаменатель:</b>'
        for znam in classes_for_znam:
            subject = await get_subject(znam.id_subject)
            shedule = await get_schedule_by_id(id_schedule=znam.id_schedule)
        
            text += f'\n{znam.class_number}. <u>{subject.name}</u>\n'
            text += f'    \nНачало пары: {str(shedule.start_time)}\nКонец пары:    {str(shedule.end_time)}\n'
            text += f'    \nСсылка на Moodle: \n{subject.moodle_link}\n'
            if subject.second_link is not None:
                text += f'    \nЗапасная ссылка: {subject.second_link}\n'
            
    return text