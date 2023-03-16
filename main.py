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
from aiogram.utils.exceptions import BotBlocked
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import inline_buttons
import peewee_mysql_connection as db_con

load_dotenv()

TOKEN = os.environ.get("TOKEN_main")
DEVELOPER_ID = int(os.environ.get("DEVELOPER_ID"))

# Set up logging
log_file = 'bot_errors.log'
logging.basicConfig(filename=log_file, level=logging.ERROR)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class MyStates(StatesGroup):
    waiting_for_message = State()
    sending_the_message = State()
    get_full_buses = State()


all_users_ids = []


def get_all_users_ids() -> None:
    for i in db_con.User.select().execute():
        all_users_ids.append(i.id)


get_all_users_ids()


async def send_message_to_people(text):
    block_counter = 0
    for user in all_users_ids:
        try:
            await bot.send_message(chat_id=user, text=f"{text}", parse_mode="HTML")
            await asyncio.sleep(0.35)
        except BotBlocked:
            block_counter += 1
    await bot.send_message(chat_id=DEVELOPER_ID, text=f"{block_counter} people blocked your bot", parse_mode="HTML")


async def check_log_file_and_send_to_developer():
    if os.stat(log_file).st_size != 0:
        with open(log_file, 'rb') as file:
            await bot.send_document(chat_id=DEVELOPER_ID, document=file)


async def donate_for_developer():
    text = """
<b>Шановні користувачі SmilaBusTime!</b>\n\nРозробник орендує сервер, на якому знаходиться бот, 
для його постійної роботи. Якщо ви є активним користувачем мого маленького проєкту та він полегшує ваше життя,
ви можете допомогти назбирати потрібну суму для щомісячної оренди. <u>Я ні в якому разі не примушую вас 
до такого кроку, ви це робите лише зі свого власного бажання.</u> Також я гарантую, що всі зібрані кошти підуть лише на 
оплату оренди серверу.\n\nЗ великою подякою, Всеволод - розробник телеграм-боту SmilaBusTime! &#10084;
    """
    await send_message_to_people(text)


async def help_developer():
    text = """
<b>Шановні користувачі SmilaBusTime!</b>\nЯкщо ви маєте інформацію про актуальний графік руху 
будь-якого автобусу, що не співпадає з тим, який надсилає вам бот, прошу надіслати інформацію розробнику за тегом: @vsevchick.\n
<b>Також не забувайте, що ви завжди можете звернутися до розробника для зауважень, прохань або реклами</b>\n
Дякую, що користуєтесь SmilaBusTime! &#10084"""
    await send_message_to_people(text)


@dp.errors_handler()
async def handle_errors(error):
    logging.error(error)


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                         reply_markup=inline_buttons.bus_inline_keyboard)
    if message.from_user.id not in all_users_ids:
        db_con.User.insert(id=message.from_user.id,
                           username=message.from_user.username,
                           first_name=message.from_user.first_name,
                           last_name=message.from_user.last_name,
                           date=datetime.datetime.now().date()).execute()
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


@dp.message_handler(content_types=["text"])
async def admin_send_message(message: types.Message):
    if message.text == "Відправити повідомлення" and message.chat.id == DEVELOPER_ID:
        await message.answer("Введіть повідомлення, яке бажаєте відправити:")
        await MyStates.waiting_for_message.set()
    elif message.text == "Назад":
        await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                             reply_markup=inline_buttons.bus_inline_keyboard)
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
        else:
            await message.answer(text="Повідомлення отримано. Бажаєте надіслати?",
                                 reply_markup=inline_buttons.confirm_reply_keyboard)
            await MyStates.next()


@dp.message_handler(state=MyStates.sending_the_message)
async def process_message_from_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['waiting_for_message']
        if message.text == "Підтвердити":
            block_counter = 0
            for user in all_users_ids:
                try:
                    await bot.send_message(chat_id=user, text=f"{text}", parse_mode="HTML")
                    await asyncio.sleep(0.35)
                except BotBlocked:
                    block_counter += 1
            await bot.send_message(chat_id=DEVELOPER_ID, text=f"{block_counter} people blocked your bot",
                                   parse_mode="HTML")
        elif message.text == "Назад":
            await bot.send_message(chat_id=DEVELOPER_ID, text="Ви повернулись до головного меню.",
                                   reply_markup=inline_buttons.admin_reply_keyboard)
            await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                                 reply_markup=inline_buttons.bus_inline_keyboard)
    await state.finish()


@dp.callback_query_handler()
async def callback_processing(callback_query: types.CallbackQuery):
    try:
        if callback_query.data == "full_bus":
            await MyStates.get_full_buses.set()
            await callback_query.message.answer(text=f"Натисніть на плитку вище з потрібним номером автобусу &#9650;",
                                                parse_mode="HTML")
        elif callback_query.data == "chat_to_developer":
            await callback_query.message.answer(text=f"Написати розробнику", parse_mode="HTML")
        else:
            bus_name = inline_buttons.dict_of_buttons_no_war[f"{callback_query.data}"]
            db_con.route_name = bus_name
            if bus_name == "route_3":
                message_text = (
                    f'Автобус було відправлено:\n'
                    f'<b>{db_con.get_departure_time_before_now_1()} {db_con.get_notes_left_before_now()} </b>із зупинки "{db_con.get_departure_point_1()}"\n'
                    f'<b>{db_con.get_departure_time_before_now_2()} {db_con.get_notes_right_before_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n'
                    f'<b>{db_con.get_departure_time_before_now_3()} {db_con.get_notes_end_before_now()} </b>із зупинки "{db_con.get_departure_point_3()}"\n\n'
                    f'Наступний автобус відправляється:\n'
                    f'<b>{db_con.get_departure_time_after_now_1()} {db_con.get_notes_left_after_now()} </b>із зупинки "{db_con.get_departure_point_1()}"\n'
                    f'<b>{db_con.get_departure_time_after_now_2()} {db_con.get_notes_right_after_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n'
                    f'<b>{db_con.get_departure_time_after_now_3()} {db_con.get_notes_end_after_now()} </b>із зупинки "{db_con.get_departure_point_3()}"\n\n'
                    f'&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}'
                )
            else:
                message_text = (
                    f'Автобус було відправлено:\n'
                    f'<b>{db_con.get_departure_time_before_now_1()} {db_con.get_notes_left_before_now()} </b>із зупинки "{db_con.get_departure_point_1()}"\n'
                    f'<b>{db_con.get_departure_time_before_now_2()} {db_con.get_notes_right_before_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n\n'
                    f'Наступний автобус відправляється:\n'
                    f'<b>{db_con.get_departure_time_after_now_1()} {db_con.get_notes_left_after_now()} </b>із зупинки "{db_con.get_departure_point_1()}"\n'
                    f'<b>{db_con.get_departure_time_after_now_2()} {db_con.get_notes_right_after_now()} </b>із зупинки "{db_con.get_departure_point_2()}"\n\n'
                    f'&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}'
                )
            await callback_query.message.answer(text=message_text,
                                                reply_markup=inline_buttons.bus_inline_keyboard,
                                                parse_mode="HTML")
    finally:
        await callback_query.answer()


@dp.callback_query_handler(state=MyStates.get_full_buses)
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        bus_name = inline_buttons.dict_of_buttons_no_war[f"{callback_query.data}"]
        db_con.route_name = bus_name
        if bus_name == "route_3":
            message_text = (
                f'Час відправлення із зупинки "{db_con.get_departure_point_1()}":\n{db_con.get_full_departure_time_1()}\n\n'
                f'Час відправлення із зупинки "{db_con.get_departure_point_2()}":\n{db_con.get_full_departure_time_2()}\n\n'
                f'Час відправлення із зупинки "{db_con.get_departure_point_3()}":\n{db_con.get_full_departure_time_3()}\n\n'
                f'&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}'
            )
        else:
            message_text = (
                f'Час відправлення із зупинки "{db_con.get_departure_point_1()}":\n{db_con.get_full_departure_time_1()}\n\n'
                f'Час відправлення із зупинки "{db_con.get_departure_point_2()}":\n{db_con.get_full_departure_time_2()}\n\n'
                f'&#x1F4C5 <b>Дні курсування</b>: {db_con.get_days()}'
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
    schedule.add_job(donate_for_developer, "cron", day_of_week="fri", hour=22, minute=00)
    schedule.add_job(help_developer, "cron", day_of_week="tue", hour=16, minute=00)
    schedule.add_job(check_log_file_and_send_to_developer, "cron", hour="8, 20")
    schedule.start()
    executor.start_polling(dp, skip_updates=True)
