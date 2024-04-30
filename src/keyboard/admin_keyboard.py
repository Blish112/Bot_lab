from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .common_keyboard import back

keyboard_start_add = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(
                text='Cтарт ⭐️', 
                callback_data='add_start_pressed'
            )
        ],
        [back]
    ]
)

keyboard_start_del = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(
                text='Cтарт ⭐️', 
                callback_data='del_start_pressed'
            )
        ],
        [back]
    ]
)