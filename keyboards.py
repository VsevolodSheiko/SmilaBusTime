from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from decouple import config

remove_keyboard = ReplyKeyboardRemove()


async def bus_keyboard():
    global buttons_under_bus_buttons, list_of_buses
    
    builder = InlineKeyboardBuilder()

    for button in list_of_buses:
        builder.add(button)
    
    for button in buttons_under_bus_buttons:
        builder.add(button)
    
    return builder.adjust(6, 6, 6, 6, 1, 1, 1).as_markup()


async def admin_start_buttons():
    global list_of_admin_buttons
    
    builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Відправити повідомлення", callback_data="admin_message"),
                InlineKeyboardButton(text="Назад", callback_data="admin_cancel"),

            ]
        ]
    )
    
    return builder.adjust(1, 1).as_markup()


async def confirm_sending_admin():
    builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Підтвердити", callback_data="accept"),
                InlineKeyboardButton(text="Назад", callback_data="back")
            ]
        ]
    )

    return builder.adjust(1).as_markup()


async def admin_attach_photo():
    builder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Так", callback_data="yes"),
                InlineKeyboardButton(text="Ні", callback_data="no")
            ]
        ]
    )

    return builder.adjust(1).as_markup()


async def location_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Надіслати геолокацію', request_location=True)
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

DEVELOPER_ID = config("DEVELOPER_ID")

list_of_buses = [
    InlineKeyboardButton(text='3', callback_data='button_3'),
    InlineKeyboardButton(text='4', callback_data='button_4'),
    InlineKeyboardButton(text='5', callback_data='button_5'),
    InlineKeyboardButton(text='17', callback_data='button_17'),
    InlineKeyboardButton(text='30', callback_data='button_30'),
    InlineKeyboardButton(text='32', callback_data='button_32'),
    InlineKeyboardButton(text='34', callback_data='button_34'),
    InlineKeyboardButton(text='39', callback_data='button_39'),
    InlineKeyboardButton(text='40', callback_data='button_40'),
    InlineKeyboardButton(text='48', callback_data='button_48'),
    InlineKeyboardButton(text='49', callback_data='button_49'),
    InlineKeyboardButton(text='126', callback_data='button_126'),
    InlineKeyboardButton(text='129', callback_data='button_129'),
    InlineKeyboardButton(text='135', callback_data='button_135'),
    InlineKeyboardButton(text='139', callback_data='button_139'),
    InlineKeyboardButton(text='140', callback_data='button_140'),
    InlineKeyboardButton(text='141', callback_data='button_141'),
    InlineKeyboardButton(text='150', callback_data='button_150'),
    InlineKeyboardButton(text='152', callback_data='button_152'),
    InlineKeyboardButton(text='153', callback_data='button_153'),
    InlineKeyboardButton(text='154', callback_data='button_154'),
    InlineKeyboardButton(text='155', callback_data='button_155'),
    InlineKeyboardButton(text='302', callback_data='button_302'),
    InlineKeyboardButton(text='309', callback_data='button_309'),
]

buttons_under_bus_buttons = [
    InlineKeyboardButton(text='Повний розклад руху', callback_data='full_bus'),
    InlineKeyboardButton(text='Найближча зупинка', callback_data='trigger_location'),
    InlineKeyboardButton(text='Написати розробнику', callback_data='chat_to_developer', url=f"tg://user?id={DEVELOPER_ID}")
]

dict_of_buttons = {
    "button_3": ("route_3", ""),
    "button_4": ("route_4", "https://www.google.com/maps/d/u/0/edit?mid=1zz64r9m2eFv75kiMI-DC02EGxm1bQfU&usp=sharing"),
    "button_5": ("route_5", "https://www.google.com/maps/d/u/0/edit?mid=1gvWIthILW36RHZRzQUZO7I51oO5GTBc&usp=sharing"),
    "button_17": ("route_17", "https://www.google.com/maps/d/u/0/edit?mid=1TcLlgwou9oaE0OhXOJ4FklBwydwtgF4&usp=sharing"),
    "button_30": ("route_30", "https://www.google.com/maps/d/u/0/edit?mid=1Axylm3JiDQ-qzY6ZHu-rlRXSiXcqEN4&usp=sharing"),
    "button_32": ("route_32", "https://www.google.com/maps/d/u/0/edit?mid=1CpFX4FecfM9Z015I2kokOMMPXXxK8fg&usp=sharing"),
    "button_34": ("route_34", "https://www.google.com/maps/d/u/0/edit?mid=1u6lpDXHjj2czMdZyBBdlQxyi_zqCQqw&usp=sharing"),
    "button_39": ("route_39", "https://www.google.com/maps/d/u/0/edit?mid=1pKQ3g4cTDu8STRN02ki4QmL1NCX2A3M&usp=sharing"),
    "button_40": ("route_40", "https://www.google.com/maps/d/u/0/edit?mid=1u4T3f9D945xSrdhDyA2jbCyaPTUBxdU&usp=sharing"),
    "button_48": ("route_48", "https://www.google.com/maps/d/u/0/edit?mid=1Sufn9IBnXK4ZdjVW8RT595f3gVrUlu8&usp=sharing"),
    "button_49": ("route_49", "https://www.google.com/maps/d/u/0/edit?mid=1vNY7jE3T9L9R2yLJdrEV8WwJ12Aqgpk&usp=sharing"),
    "button_126": ("route_126", "https://www.google.com/maps/d/u/0/edit?mid=1EVKgAtZtETezea5x_Fiq_WywADnWxOg&usp=sharing"),
    "button_129": ("route_129", "https://www.google.com/maps/d/u/0/edit?mid=1flhYid0lA1DdwpGkzWAiVIvPANdvwH8&usp=sharing"),
    "button_135": ("route_135", "https://www.google.com/maps/d/u/0/edit?mid=1ZEuKc6XE_JHA6nLMoQ222EHpRKOwz-U&usp=sharing"),
    "button_139": ("route_139", "https://www.google.com/maps/d/u/0/edit?mid=1q6ZjVgWvbiSBuM76kopF3-zxb5yGCOM&usp=sharing"),
    "button_140": ("route_140", "https://www.google.com/maps/d/u/0/edit?mid=1qhRhrJeRsp02n-9g26-A7UXK72zb2dQ&usp=sharing"),
    "button_141": ("route_141", "https://www.google.com/maps/d/u/0/edit?mid=1nk-l9rrqywfpVgao7AubXN8oimLRRYU&usp=sharing"),
    "button_150": ("route_150", "https://www.google.com/maps/d/u/0/edit?mid=1KnfPme6iFu-QfTLoZ56c3UdL7XnKF4s&usp=sharing"),
    "button_152": ("route_152", "https://www.google.com/maps/d/u/0/edit?mid=1OUB3ObaSUZta2r9cvcdMvd1yCMVXqNM&usp=sharing"),
    "button_153": ("route_153", "https://www.google.com/maps/d/u/0/edit?mid=1NAQfwb_ocf0mbwfMS4sFHlkH9l292T4&usp=sharing"),
    "button_154": ("route_154", "https://www.google.com/maps/d/u/0/edit?mid=1WpJc0-cVC_6F1Dn1pi7bJLy4cdkS31c&usp=sharing"),
    "button_155": ("route_155", "https://www.google.com/maps/d/u/0/edit?mid=1k3aEP47nIHOoYwKOw0S6a8CMqWc6nNo&usp=sharing"),
    "button_302": ("route_302", "https://www.google.com/maps/d/u/0/edit?mid=1SqOR3qkr7GEEgsJ-oVSngcTEC7XtSUI&usp=sharing"),
    "button_309": ("route_309", "https://www.google.com/maps/d/u/0/edit?mid=18WTkDF8PcJju6Im6cK6rnelYsBE5ZVM&usp=sharing"),
}
