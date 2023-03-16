from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os
bus_inline_keyboard = InlineKeyboardMarkup(row_width=6)
admin_reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
confirm_reply_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

load_dotenv()
DEVELOPER_ID = int(os.environ.get("DEVELOPER_ID"))
list_of_buttons = [
    InlineKeyboardButton('3', callback_data='button_3'),
    InlineKeyboardButton('4', callback_data='button_4'),
    InlineKeyboardButton('5', callback_data='button_5'),
    InlineKeyboardButton('17', callback_data='button_17'),
    InlineKeyboardButton('30', callback_data='button_30'),
    InlineKeyboardButton('32', callback_data='button_32'),
    InlineKeyboardButton('34', callback_data='button_34'),
    InlineKeyboardButton('39', callback_data='button_39'),
    InlineKeyboardButton('40', callback_data='button_40'),
    InlineKeyboardButton('48', callback_data='button_48'),
    InlineKeyboardButton('49', callback_data='button_49'),
    InlineKeyboardButton('126', callback_data='button_126'),
    InlineKeyboardButton('129', callback_data='button_129'),
    InlineKeyboardButton('139', callback_data='button_139'),
    InlineKeyboardButton('140', callback_data='button_140'),
    InlineKeyboardButton('141', callback_data='button_141'),
    InlineKeyboardButton('150', callback_data='button_150'),
    InlineKeyboardButton('153', callback_data='button_153'),
    InlineKeyboardButton('154', callback_data='button_154'),
    InlineKeyboardButton('155', callback_data='button_155'),
    InlineKeyboardButton('302', callback_data='button_302'),
    InlineKeyboardButton('309', callback_data='button_309'),
]

full_time_button = InlineKeyboardButton('Повний розклад руху', callback_data='full_bus')
chat_with_developer = InlineKeyboardButton('Написати розробнику', callback_data='chat_to_developer',
                                           url=f"tg://user?id={DEVELOPER_ID}")

list_of_admin_buttons = [
    KeyboardButton("Відправити повідомлення"),
    KeyboardButton("Назад"),
]


dict_of_buttons_no_war = {
    "button_3": "route_3",
    "button_4": "route_4",
    "button_5": "route_5",
    "button_17": "route_17",
    "button_30": "route_30",
    "button_32": "route_32",
    "button_34": "route_34",
    "button_39": "route_39",
    "button_40": "route_40",
    "button_48": "route_48",
    "button_49": "route_49",
    "button_126": "route_126",
    "button_129": "route_129",
    "button_139": "route_139",
    "button_140": "route_140",
    "button_141": "route_141",
    "button_150": "route_150",
    "button_153": "route_153",
    "button_154": "route_154",
    "button_155": "route_155",
    "button_302": "route_302",
    "button_309": "route_309",

}

for button in list_of_buttons:
    bus_inline_keyboard.insert(button)

bus_inline_keyboard.row(full_time_button)
bus_inline_keyboard.row(chat_with_developer)

for button in list_of_admin_buttons:
    admin_reply_keyboard.insert(button)

confirm_reply_keyboard.add(KeyboardButton("Підтвердити"), KeyboardButton("Назад"))
