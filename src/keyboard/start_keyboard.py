from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = [
    [
        KeyboardButton(text="Расписание 📗"),
        KeyboardButton(text="Верификация 🔐")
    ],
    [
        KeyboardButton(text="Справка по разделам 📕")
    ]
]

keyboard_start_help = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )