from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

import mysql_connection as db_con
from states.appstates import MyStates
import keyboards
from location_data import bus_stops
from .other_functions import calculate_distance

router = Router()

@router.message(F.location)
async def handle_location(message: types.Message):
    closest_point = None
    min_distance = float('inf')
    location_global = message.location
    for point in bus_stops:
        point_latitude = point[0][0]
        point_longitude = point[0][1]
        distance = await calculate_distance(location_global.latitude, location_global.longitude, point_latitude, point_longitude)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    await message.reply_location(latitude=closest_point[0][0], longitude=closest_point[0][1])
    await message.answer(text=f"&#128652 Автобусні маршрути: {closest_point[1]}", parse_mode="HTML")
    await db_con.update_location(message.from_user.id, location_global=f"{location_global.latitude} {location_global.longitude}")


@router.message(MyStates.waiting_for_message)
async def process_message_from_admin(message: types.Message, state: FSMContext):
    await state.update_data(message_from_admin=message.text)
    await message.answer(text="Повідомлення отримано. Бажаєте прикріпити фото?",
                            reply_markup=await keyboards.admin_attach_photo())
    await state.set_state(MyStates.ask_for_photo)


@router.message(F.photo, MyStates.waiting_for_photo)
async def process_photo_from_admin(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await message.answer(text="Фото отримано. Бажаєте надіслати?",
                            reply_markup=await keyboards.confirm_sending_admin())
    await state.set_state(MyStates.sending_the_message)


