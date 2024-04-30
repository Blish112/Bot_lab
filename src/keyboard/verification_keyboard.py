from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .common_keyboard import back

keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(
                text='Назад ↩️', 
                callback_data='start_back_pressed'
            )
        ]
    ]
)

keyboard_verification = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(
                text='Cтарт ⭐️', 
                callback_data='start_pressed'
            )
        ],
        [back]
    ]
)

keyboard_verification_restart = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(
                text='Изменить номер группы ♻️', 
                callback_data='restart_pressed'
            )
        ],
        [   
            InlineKeyboardButton(
                text='Продолжить ⌨️', 
                callback_data='continue_pressed'
            )
        ],
        [back]
    ]
)