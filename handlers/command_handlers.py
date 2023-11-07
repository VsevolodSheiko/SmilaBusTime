from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from decouple import config
from datetime import datetime

import mysql_connection as db_con
import keyboards
from states.appstates import MyStates

router = Router()
bot = Bot(config("TOKEN_test"))
DEVELOPER_ID = int(config("DEVELOPER_ID"))


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(text="Оновлення даних...",
                         reply_markup=keyboards.remove_keyboard)
    
    await message.answer(text="Будь ласка, оберіть номер потрібного автобусу з плиток нижче:",
                         reply_markup=await keyboards.bus_keyboard())
    await db_con.get_all_users_ids()
    if message.from_user.id not in db_con.all_users_ids:
        await db_con.insert_new_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            datetime.now()
        )
    else:
        await db_con.update_date_existing_user(message.from_user.id, datetime.now())


@router.message(Command("admin"))
async def admin(message: types.Message, state: FSMContext):
    await db_con.get_all_users_ids()
    if message.from_user.id == DEVELOPER_ID:
        await message.answer(text="Вітаю у адмін-панелі розробника.",
                             reply_markup=await keyboards.admin_start_buttons())
        await state.set_state(MyStates.admin)
    else:
        await message.answer(text="У вас немає доступу до адміністративної панелі.",
                             reply_markup=await keyboards.bus_keyboard())