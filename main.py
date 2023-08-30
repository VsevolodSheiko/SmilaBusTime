import datetime
import os
import asyncio
import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from math import sin, cos, sqrt, atan2, radians

import inline_buttons
import peewee_mysql_connection as db_con
from location_data import bus_stops

load_dotenv()

TOKEN = os.environ.get("TOKEN_main")
DEVELOPER_ID = int(os.environ.get("DEVELOPER_ID"))

# Set up logging
log_file = 'bot_errors.log'
logging.basicConfig(filename=log_file, level=logging.ERROR)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

file_path = None

class MyStates(StatesGroup):
    waiting_for_message = State()
    ask_for_photo = State()
    waiting_for_photo = State()
    sending_the_message = State()
    
    get_full_buses = State()


all_users_ids = []


def get_all_users_ids() -> None:
    global all_users_ids
    all_users_ids.clear()
    for i in db_con.User.select().execute():
        all_users_ids.append(i.id)
    if len(all_users_ids) != 0:
        all_users_ids = list(set(all_users_ids))
    

get_all_users_ids()


async def send_message_to_people(text, photo = None):
    block_counter = 0
    for user in all_users_ids:
        try:
            if photo is None:
                await bot.send_message(chat_id=user, text=text, parse_mode="HTML")
            else:
                await bot.send_photo(chat_id=user, photo=photo, caption=text, parse_mode="HTML")
            await asyncio.sleep(0.3)
        except exceptions.BotBlocked:
            block_counter += 1
            db_con.User.delete().where(db_con.User.id == user).execute()
        except exceptions.ChatNotFound:
            block_counter += 1
            db_con.User.delete().where(db_con.User.id == user).execute()
        except exceptions.RetryAfter as e:
            block_counter += 1
            await asyncio.sleep(e.timeout)
        except exceptions.UserDeactivated:
            block_counter += 1
            db_con.User.delete().where(db_con.User.id == user).execute()
        except exceptions.TelegramAPIError:
            block_counter += 1
        else:
            pass
    await bot.send_message(chat_id=DEVELOPER_ID, text=f"{block_counter} people blocked your bot", parse_mode="HTML")


async def check_log_file_and_send_to_developer():
    await bot.send_message(chat_id=DEVELOPER_ID, text=f"{db_con.get_clicks_count()}")
    if os.stat(log_file).st_size != 0:
        with open(log_file, 'rb') as file:
            await bot.send_document(chat_id=DEVELOPER_ID, document=file)


async def clear_log_file():
    if os.stat(log_file).st_size != 0:
        with open(log_file, 'w') as file:
            file.truncate(0)


async def set_clickers_to_zero():
    db_con.set_clickers_to_zero()


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
Дякую, що користуєтесь SmilaBusTime! &#10084"""
    await send_message_to_people(text)


@dp.errors_handler()
async def handle_errors(error, *args):
    logging.error(error, args)


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(text="Оновлення даних...",
                         reply_markup=inline_buttons.delete_old_keyboard)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                         reply_markup=inline_buttons.bus_inline_keyboard)
    print(datetime.datetime.now().date(), all_users_ids, sep="\n")
    if message.from_user.id not in all_users_ids:
        db_con.User.insert(id=message.from_user.id,
                           username=message.from_user.username,
                           first_name=message.from_user.first_name,
                           last_name=message.from_user.last_name,
                           date=datetime.datetime.now().date(),
                           location=None).execute()
    else:
        db_con.User.update(date=datetime.datetime.now().date()).where(db_con.User.id == message.from_user.id).execute()


@dp.message_handler(Command("admin"))
async def admin(message: types.Message):
    if message.chat.id == DEVELOPER_ID:
        await message.answer(text="Вітаю у адмін-панелі розробника.",
                             reply_markup=inline_buttons.admin_reply_keyboard)

    else:
        await message.answer(text="На жаль, у вас немає доступу до адміністративної панелі.",
                             reply_markup=inline_buttons.bus_inline_keyboard)


def calculate_distance(lat1, lon1, lat2, lon2):
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


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.answer(text="Оновлення даних...", reply_markup=inline_buttons.delete_old_keyboard)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    closest_point = None
    min_distance = float('inf')
    location_global = message.location
    for point in bus_stops:
        point_latitude = point[0][0]
        point_longitude = point[0][1]
        distance = calculate_distance(location_global.latitude, location_global.longitude, point_latitude, point_longitude)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    await message.reply_location(latitude=closest_point[0][0], longitude=closest_point[0][1])
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text=f"&#128652 Автобусні маршрути: {closest_point[1]}", parse_mode="HTML")
    db_con.User.update(location = f"{location_global.latitude} {location_global.longitude}").where(db_con.User.id == message.from_user.id).execute()
    


@dp.message_handler(content_types=types.ContentType.TEXT)
async def admin_send_message(message: types.Message):
    if message.text == "Відправити повідомлення" and message.chat.id == DEVELOPER_ID:
        await message.answer("Введіть повідомлення, яке бажаєте відправити:")
        await MyStates.waiting_for_message.set()
    
    else:
        await message.answer(text="Вибачте, виникла помилка. Спробуйте ще раз.",
                             reply_markup=inline_buttons.bus_inline_keyboard)


@dp.message_handler(state=MyStates.waiting_for_message)
async def process_message_from_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['waiting_for_message'] = message.text
        if message.text == "Назад":
            await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                                 reply_markup=inline_buttons.bus_inline_keyboard)
            await state.finish()
        else:
            await message.answer(text="Повідомлення отримано. Бажаєте прикріпити фото?",
                                 reply_markup=inline_buttons.confirm_reply_keyboard_2)
            await MyStates.ask_for_photo.set()


@dp.message_handler(state=MyStates.ask_for_photo)
async def asking_for_photo_from_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Ні":
            await message.answer(text="Бажаєте надіслати повідомлення?",
                                 reply_markup=inline_buttons.confirm_reply_keyboard)
            await MyStates.sending_the_message.set()
        else:
            await message.answer(text="Будь ласка, надішліть фото.")
            await MyStates.waiting_for_photo.set()


@dp.message_handler(state=MyStates.waiting_for_photo, content_types=types.ContentType.PHOTO)
async def process_photo_from_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        
        # Create directory to save received images
        DOWNLOADS_DIR = "downloaded_content"  
        if not os.path.exists(DOWNLOADS_DIR):
            os.makedirs(DOWNLOADS_DIR)
        picture = message.photo[-1]
        file_unique_id = picture.file_unique_id

        # Download the photo to the specified directory
        global file_path
        file_path = os.path.join(DOWNLOADS_DIR, f"{file_unique_id}.jpg")
        await picture.download(destination_file=file_path)
        await message.answer(text="Фото отримано. Бажаєте надіслати?",
                                reply_markup=inline_buttons.confirm_reply_keyboard_2)
        await MyStates.sending_the_message.set()


@dp.message_handler(state=MyStates.sending_the_message)
async def final_message_sending(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Так":
            with open(file_path, 'rb') as photo_file:
                photo_data = photo_file.read()
                await send_message_to_people(text=data["waiting_for_message"], photo=photo_data)
        elif message.text == "Ні":
            await message.answer("Ви повернулись до головного меню. Останнє збережене фото було очищене.",
                                reply_markup=inline_buttons.bus_inline_keyboard)
        elif message.text == "Підтвердити":
            await send_message_to_people(text=data["waiting_for_message"])
        else:
            await message.answer("Вибачте, виникла помилка.", reply_markup=inline_buttons.bus_inline_keyboard)
        await state.finish()
            


@dp.callback_query_handler()
async def callback_processing(callback_query: types.CallbackQuery):
    try:
        if callback_query.data == "full_bus":
            await MyStates.get_full_buses.set()
            await callback_query.message.answer(
                text="Натисніть на плитку вище з потрібним номером автобусу &#9650;",
                parse_mode="HTML",
            )
        elif callback_query.data == "chat_to_developer":
            await callback_query.message.answer(
                text="Написати розробнику", parse_mode="HTML"
            )
        elif callback_query.data == "trigger_location":
            await callback_query.message.answer(
                "Натисніть кнопку знизу, щоб надіслати свою геолокацію. <u>Обов'язково</u> увімкніть на телефоні службу GPS(місцезнаходження)!",
                reply_markup=inline_buttons.location_keyboard,
                parse_mode="HTML")
        else:
            bus_name = inline_buttons.dict_of_buttons[f"{callback_query.data}"]
            db_con.route_name = bus_name
            if bus_name == "route_3":
                db_con.get_and_update_clicks(bus_name)
                message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>\n
Автобус було відправлено:
<b>{db_con.get_departure_time_before_now_1()} {db_con.get_notes_left_before_now()} </b>із зупинки "{db_con.get_departure_point_1()}"
<b>{db_con.get_departure_time_before_now_2()} {db_con.get_notes_right_before_now()} </b>із зупинки "{db_con.get_departure_point_2()}"
<b>{db_con.get_departure_time_before_now_3()} {db_con.get_notes_end_before_now()} </b>із зупинки "{db_con.get_departure_point_3()}"\n
Наступний автобус відправляється:
<b>{db_con.get_departure_time_after_now_1()} {db_con.get_notes_left_after_now()} </b>із зупинки "{db_con.get_departure_point_1()}"
<b>{db_con.get_departure_time_after_now_2()} {db_con.get_notes_right_after_now()} </b>із зупинки "{db_con.get_departure_point_2()}"
<b>{db_con.get_departure_time_after_now_3()} {db_con.get_notes_end_after_now()} </b>із зупинки "{db_con.get_departure_point_3()}"\n
&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}"""
                                )
            else:
                message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>\n
Автобус було відправлено:
<b>{db_con.get_departure_time_before_now_1()} {db_con.get_notes_left_before_now()} </b>із зупинки "{db_con.get_departure_point_1()}"
<b>{db_con.get_departure_time_before_now_2()} {db_con.get_notes_right_before_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n
Наступний автобус відправляється:
<b>{db_con.get_departure_time_after_now_1()} {db_con.get_notes_left_after_now()} </b>із зупинки "{db_con.get_departure_point_1()}"
<b>{db_con.get_departure_time_after_now_2()} {db_con.get_notes_right_after_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n
&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}"""
                                )
            db_con.get_and_update_clicks(bus_name)
            await callback_query.message.answer(
                text=f'<a href="{inline_buttons.buttons_links[callback_query.data]}">&#128506 Маршрут автобуса на карті</a>',
                parse_mode="HTML")
            await callback_query.message.answer(text=message_text,
                                                reply_markup=inline_buttons.bus_inline_keyboard,
                                                parse_mode="HTML")
    finally:
        await callback_query.answer()


@dp.callback_query_handler(state=MyStates.get_full_buses)
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        bus_name = inline_buttons.dict_of_buttons[f"{callback_query.data}"]
        db_con.route_name = bus_name
        if bus_name == "route_3":
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>
Час відправлення із зупинки "{db_con.get_departure_point_1()}":\n{db_con.get_full_departure_time_1()}\n
Час відправлення із зупинки "{db_con.get_departure_point_2()}":\n{db_con.get_full_departure_time_2()}\n
Час відправлення із зупинки "{db_con.get_departure_point_3()}":\n{db_con.get_full_departure_time_3()}\n
&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}"""
                            )
        else:
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>
Час відправлення із зупинки "{db_con.get_departure_point_1()}":\n{db_con.get_full_departure_time_1()}\n
Час відправлення із зупинки "{db_con.get_departure_point_2()}":\n{db_con.get_full_departure_time_2()}\n
&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}"""
                            )
        await callback_query.message.answer(text=message_text,
                                            reply_markup=inline_buttons.bus_inline_keyboard,
                                            parse_mode='HTML')
        await state.finish()
    except KeyError:
        await callback_query.message.answer(text="Ви не обрали автобус. Будь ласка, повторіть спробу.",
                                            reply_markup=inline_buttons.bus_inline_keyboard)
    finally:
        await callback_query.answer()


if __name__ == "__main__":
    schedule = AsyncIOScheduler()
    schedule.add_job(donate_for_developer, "cron", day=25, hour=20)
    schedule.add_job(get_all_users_ids, "interval", seconds=15)
    schedule.add_job(help_developer, "cron", day_of_week="tue", hour=20, minute=00)
    schedule.add_job(check_log_file_and_send_to_developer, "cron", hour=22)
    schedule.add_job(clear_log_file, "cron", hour=22, minute=1)
    schedule.add_job(set_clickers_to_zero, "cron", hour=1)
    schedule.start()
    executor.start_polling(dp, skip_updates=True)
