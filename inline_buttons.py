from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv
import os

bus_inline_keyboard = InlineKeyboardMarkup(row_width=6)
admin_reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
confirm_reply_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
confirm_reply_keyboard_2 = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
delete_old_keyboard = ReplyKeyboardRemove()



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
    InlineKeyboardButton('135', callback_data='button_135'),
    InlineKeyboardButton('139', callback_data='button_139'),
    InlineKeyboardButton('140', callback_data='button_140'),
    InlineKeyboardButton('141', callback_data='button_141'),
    InlineKeyboardButton('150', callback_data='button_150'),
    InlineKeyboardButton('152', callback_data='button_152'),
    InlineKeyboardButton('153', callback_data='button_153'),
    InlineKeyboardButton('154', callback_data='button_154'),
    InlineKeyboardButton('155', callback_data='button_155'),
    InlineKeyboardButton('302', callback_data='button_302'),
    InlineKeyboardButton('309', callback_data='button_309'),
]

full_time_button = InlineKeyboardButton('Повний розклад руху', callback_data='full_bus')
chat_with_developer = InlineKeyboardButton('Написати розробнику', callback_data='chat_to_developer',
                                           url=f"tg://user?id={DEVELOPER_ID}")
trigger_location_button = InlineKeyboardButton('Найближча зупинка', callback_data='trigger_location')

list_of_admin_buttons = [
    KeyboardButton("Відправити повідомлення"),
    KeyboardButton("Назад"),
]


list_of_admin_buttons_2 = [
    KeyboardButton("Так"),
    KeyboardButton("Ні")
]
    


dict_of_buttons = {
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
    "button_135": "route_135",
    "button_139": "route_139",
    "button_140": "route_140",
    "button_141": "route_141",
    "button_150": "route_150",
    "button_152": "route_152",
    "button_153": "route_153",
    "button_154": "route_154",
    "button_155": "route_155",
    "button_302": "route_302",
    "button_309": "route_309",

}

buttons_links = {
    "button_3": "",
    "button_4": "https://www.google.com/maps/d/u/0/edit?mid=1zz64r9m2eFv75kiMI-DC02EGxm1bQfU&usp=sharing",
    "button_5": "https://www.google.com/maps/d/u/0/edit?mid=1gvWIthILW36RHZRzQUZO7I51oO5GTBc&usp=sharing",
    "button_17": "https://www.google.com/maps/d/u/0/edit?mid=1TcLlgwou9oaE0OhXOJ4FklBwydwtgF4&usp=sharing",
    "button_30": "https://www.google.com/maps/d/u/0/edit?mid=1Axylm3JiDQ-qzY6ZHu-rlRXSiXcqEN4&usp=sharing",
    "button_32": "https://www.google.com/maps/d/u/0/edit?mid=1CpFX4FecfM9Z015I2kokOMMPXXxK8fg&usp=sharing",
    "button_34": "https://www.google.com/maps/d/u/0/edit?mid=1u6lpDXHjj2czMdZyBBdlQxyi_zqCQqw&usp=sharing",
    "button_39": "https://www.google.com/maps/d/u/0/edit?mid=1pKQ3g4cTDu8STRN02ki4QmL1NCX2A3M&usp=sharing",
    "button_40": "https://www.google.com/maps/d/u/0/edit?mid=1u4T3f9D945xSrdhDyA2jbCyaPTUBxdU&usp=sharing",
    "button_48": "https://www.google.com/maps/d/u/0/edit?mid=1Sufn9IBnXK4ZdjVW8RT595f3gVrUlu8&usp=sharing",
    "button_49": "https://www.google.com/maps/d/u/0/edit?mid=1vNY7jE3T9L9R2yLJdrEV8WwJ12Aqgpk&usp=sharing",
    "button_126": "https://www.google.com/maps/d/u/0/edit?mid=1EVKgAtZtETezea5x_Fiq_WywADnWxOg&usp=sharing",
    "button_129": "https://www.google.com/maps/d/u/0/edit?mid=1flhYid0lA1DdwpGkzWAiVIvPANdvwH8&usp=sharing",
    "button_135": "https://www.google.com/maps/d/u/0/edit?mid=1ZEuKc6XE_JHA6nLMoQ222EHpRKOwz-U&usp=sharing",
    "button_139": "https://www.google.com/maps/d/u/0/edit?mid=1q6ZjVgWvbiSBuM76kopF3-zxb5yGCOM&usp=sharing",
    "button_140": "https://www.google.com/maps/d/u/0/edit?mid=1qhRhrJeRsp02n-9g26-A7UXK72zb2dQ&usp=sharing",
    "button_141": "https://www.google.com/maps/d/u/0/edit?mid=1nk-l9rrqywfpVgao7AubXN8oimLRRYU&usp=sharing",
    "button_150": "https://www.google.com/maps/d/u/0/edit?mid=1KnfPme6iFu-QfTLoZ56c3UdL7XnKF4s&usp=sharing",
    "button_152": "https://www.google.com/maps/d/u/0/edit?mid=1OUB3ObaSUZta2r9cvcdMvd1yCMVXqNM&usp=sharing",
    "button_153": "https://www.google.com/maps/d/u/0/edit?mid=1NAQfwb_ocf0mbwfMS4sFHlkH9l292T4&usp=sharing",
    "button_154": "https://www.google.com/maps/d/u/0/edit?mid=1WpJc0-cVC_6F1Dn1pi7bJLy4cdkS31c&usp=sharing",
    "button_155": "https://www.google.com/maps/d/u/0/edit?mid=1k3aEP47nIHOoYwKOw0S6a8CMqWc6nNo&usp=sharing",
    "button_302": "https://www.google.com/maps/d/u/0/edit?mid=1SqOR3qkr7GEEgsJ-oVSngcTEC7XtSUI&usp=sharing",
    "button_309": "https://www.google.com/maps/d/u/0/edit?mid=18WTkDF8PcJju6Im6cK6rnelYsBE5ZVM&usp=sharing",

}



for button in list_of_buttons:
    bus_inline_keyboard.insert(button)

bus_inline_keyboard.row(full_time_button)
bus_inline_keyboard.row(trigger_location_button)
bus_inline_keyboard.row(chat_with_developer)


for button in list_of_admin_buttons:
    admin_reply_keyboard.insert(button)

confirm_reply_keyboard.add(KeyboardButton("Підтвердити"), KeyboardButton("Назад"))
confirm_reply_keyboard_2.add(KeyboardButton("Так"), KeyboardButton("Ні"))
location_keyboard.insert(KeyboardButton("Надіслати геолокацію", request_location=True))
