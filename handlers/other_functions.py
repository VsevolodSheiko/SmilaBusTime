import asyncio
from aiogram.exceptions import AiogramError
from math import sin, cos, sqrt, atan2, radians
from decouple import config

import mysql_connection as db_con

from .command_handlers import bot
DEVELOPER_ID = int(config("DEVELOPER_ID"))

async def calculate_distance(lat1, lon1, lat2, lon2):
    # Approximate radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calculate the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance in kilometers
    return R * c

async def send_message_to_people(text, photo = None):
    counter = 0
    for user in db_con.all_users_ids:
        try:
            if photo is None:
                await bot.send_message(chat_id=user, text=text)
            else:
                await bot.send_photo(chat_id=user, photo=photo, caption=text)
            #await asyncio.sleep(0.3)
        except AiogramError as error:
            print(error)
            counter += 1
    await bot.send_message(
        chat_id=DEVELOPER_ID, 
        text=f"Кількість помилок при надсиланні повідомлення: {counter}")


async def check_log_file_and_send_to_developer():
    log_file = 'bot_errors.log'
    await bot.send_message(chat_id=DEVELOPER_ID, text=f"{await db_con.get_clicks_count()}")
    if os.stat(log_file).st_size != 0:
        with open(log_file, 'rb') as file:
            await bot.send_document(chat_id=DEVELOPER_ID, document=file)


async def clear_log_file():
    if os.stat(log_file).st_size != 0:
        with open(log_file, 'w') as file:
            await file.truncate(0)


async def donate_for_developer():
    text = """
<b>Шановні користувачі SmilaBusTime!</b>\n\nРозробник орендує сервер, на якому знаходиться бот, 
для його постійної роботи. Якщо ви є активним користувачем мого маленького проєкту та він полегшує ваше життя,
ви можете допомогти назбирати потрібну суму для щомісячної оренди. <u>Я ні в якому разі не примушую вас 
до такого кроку, ви це робите лише зі свого власного бажання.</u>\n\nЗ великою подякою, Всеволод - розробник телеграм-боту SmilaBusTime! &#10084\n
<a href="https://send.monobank.ua/8DgxnTfLuK">&#128179 Картка монобанку</a>;
    """
    await send_message_to_people(text)


async def help_developer():
    text = """
<b>Шановні користувачі SmilaBusTime!</b>\nЯкщо ви маєте інформацію про актуальний графік руху 
будь-якого автобусу, що не співпадає з тим, який надсилає вам бот, прошу надіслати інформацію розробнику за тегом: @vsevolodsheiko.\n
<b>Також не забувайте, що ви завжди можете звернутися до розробника для <u>реклами</u>, зауважень та прохань</b>\n
Дякую, що користуєтесь SmilaBusTime! &#10084
    """
    await send_message_to_people(text)