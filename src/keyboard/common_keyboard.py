from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

back = InlineKeyboardButton(text='Вернуться на стартовую страницу ↩️', callback_data='back_pressed')
common_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back]])