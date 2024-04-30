from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from .common_keyboard import back

class WeekdayCallbackFactory(CallbackData, prefix="weekday"):
    weekday: str
    num_weekday: Optional[int] = None

def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    
    # row 1
    builder.button(text='Cегодня', callback_data=WeekdayCallbackFactory(weekday="Сегодня"))
    builder.button(text='Завтра', callback_data=WeekdayCallbackFactory(weekday="Завтра"))
    builder.button(text='Числ/Знам', callback_data='chis_znam_pressed')
    
    # row 2
    builder.button(text='Понедельник', callback_data=WeekdayCallbackFactory(weekday='Понедельник', num_weekday=1))
    builder.button(text='Вторник', callback_data=WeekdayCallbackFactory(weekday='Вторник', num_weekday=2))
    builder.button(text='Среда', callback_data=WeekdayCallbackFactory(weekday='Среда', num_weekday=3))
    
    # row 3
    builder.button(text='Четверг', callback_data=WeekdayCallbackFactory(weekday='Четверг', num_weekday=4))
    builder.button(text='Пятница', callback_data=WeekdayCallbackFactory(weekday='Пятница', num_weekday=5))
    builder.button(text='Суббота', callback_data=WeekdayCallbackFactory(weekday='Суббота', num_weekday=6))
    
    # row 4
    builder.add(back)
    
    builder.adjust(3)
    return builder.as_markup()
