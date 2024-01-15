from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_buttons = [KeyboardButton(text='Парсить')]
KB_MENU = ReplyKeyboardMarkup(keyboard=[menu_buttons], resize_keyboard=True)

mode_buttons = [KeyboardButton(text='Продолжительный'), KeyboardButton(text='Одноразовый')]
KB_MODE = ReplyKeyboardMarkup(keyboard=[mode_buttons], resize_keyboard=True)

KB_ALL_PAGES = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Все')]], resize_keyboard=True)

rkr = ReplyKeyboardRemove()