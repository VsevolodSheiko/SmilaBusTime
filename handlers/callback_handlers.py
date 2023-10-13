from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.exceptions import AiogramError

from states.appstates import MyStates
from .other_functions import send_message_to_people
import keyboards
import mysql_connection as db_con

router = Router()

@router.callback_query(MyStates.admin)
async def admin_send_message(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "admin_message":
        await callback_query.message.edit_text("Введіть повідомлення, яке бажаєте відправити:")
        await state.set_state(MyStates.waiting_for_message)
    elif callback_query.data == "back":
        await callback_query.message.edit_text(
            "Ви вийшли з режиму адміна.",
            reply_markup=await keyboards.bus_keyboard()
            )
        await state.finish()
    else:
        await callback_query.message.answer(
            text="Виникла помилка. Спробуйте ще раз.",
            reply_markup=await keyboards.bus_keyboard())
        await state.clear()
    await callback_query.answer()


@router.callback_query(MyStates.ask_for_photo)
async def asking_for_photo_from_admin(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "no":
        await callback_query.message.edit_text(text="Бажаєте надіслати повідомлення?",
                                reply_markup=await keyboards.confirm_sending_admin())
        await state.set_state(MyStates.sending_the_message)
    else:
        await callback_query.message.edit_text(text="Будь ласка, надішліть фото.")
        await state.set_state(MyStates.waiting_for_photo)
    await callback_query.answer()


@router.callback_query(MyStates.sending_the_message)
async def final_message_sending(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback_query.data == "yes":
        await send_message_to_people(text=data["message_from_admin"], photo=data['photo_id'])
    elif callback_query.data in ["no", "back"]:
        await callback_query.message.edit_text("Ви повернулись до головного меню. Останнє збережене фото було очищене.",
                            reply_markup=await keyboards.bus_keyboard())
    elif callback_query.data == "accept":
        await send_message_to_people(text=data["message_from_admin"])
    else:
        await callback_query.message.answer("Вибачте, виникла помилка.", reply_markup=await keyboards.bus_keyboard())
    await callback_query.answer()
    await state.finish()


@router.callback_query(F.data == "full_bus")
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text="Натисніть на плитку вище з потрібним номером автобусу &#9650;",
        parse_mode="HTML",
    )
    await state.set_state(MyStates.get_full_buses)
    await callback_query.answer()


@router.callback_query(MyStates.get_full_buses, F.data.startswith("button_"))
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        bus_name = keyboards.dict_of_buttons[callback_query.data][0]
        db_con.route_name = bus_name
        if bus_name == "route_3":
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>
Час відправлення із зупинки "{await db_con.get_departure_point_1()}":\n{await db_con.get_full_departure_time_1()}\n
Час відправлення із зупинки "{await db_con.get_departure_point_2()}":\n{await db_con.get_full_departure_time_2()}\n
Час відправлення із зупинки "{await db_con.get_departure_point_3()}":\n{await db_con.get_full_departure_time_3()}\n
&#x1F4C5 <b>Дні курсування</b>: {await db_con.get_days()}"""
                            )
        else:
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>
Час відправлення із зупинки "{await db_con.get_departure_point_1()}":\n{await db_con.get_full_departure_time_1()}\n
Час відправлення із зупинки "{await db_con.get_departure_point_2()}":\n{await db_con.get_full_departure_time_2()}\n
&#x1F4C5 <b>Дні курсування</b>: {await db_con.get_days()}"""
                            )
        await callback_query.message.answer(text=message_text,
                                            reply_markup=await keyboards.bus_keyboard(),
                                            parse_mode='HTML')
        await state.clear()
    except KeyError:
        await callback_query.message.answer(text="Ви не обрали автобус. Будь ласка, повторіть спробу.",
                                            reply_markup=await keyboards.bus_keyboard())
    finally:
        await state.clear()
        await callback_query.answer()


@router.callback_query(F.data == "trigger_location")
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        "Натисніть кнопку знизу, щоб надіслати свою геолокацію. <u>Обов'язково</u> увімкніть на телефоні службу GPS(місцезнаходження)!",
        reply_markup=await keyboards.location_reply_keyboard(),
        parse_mode="HTML")
    await callback_query.answer()


@router.callback_query(F.data.startswith("button"))
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        bus_name = keyboards.dict_of_buttons[f"{callback_query.data}"][0]
        db_con.route_name = bus_name
        await db_con.get_and_update_clicks(bus_name)
        if bus_name == "route_3":
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>\n
Автобус було відправлено:
<b>{await db_con.get_departure_time_before_now_1()} {await db_con.get_notes_left_before_now()} </b>із зупинки "{await db_con.get_departure_point_1()}"
<b>{await db_con.get_departure_time_before_now_2()} {await db_con.get_notes_right_before_now()} </b>із зупинки "{await db_con.get_departure_point_2()}"
<b>{await db_con.get_departure_time_before_now_3()} {await db_con.get_notes_end_before_now()} </b>із зупинки "{await db_con.get_departure_point_3()}"\n
Наступний автобус відправляється:
<b>{await db_con.get_departure_time_after_now_1()} {await db_con.get_notes_left_after_now()} </b>із зупинки "{await db_con.get_departure_point_1()}"
<b>{await db_con.get_departure_time_after_now_2()} {await db_con.get_notes_right_after_now()} </b>із зупинки "{await db_con.get_departure_point_2()}"
<b>{await db_con.get_departure_time_after_now_3()} {await db_con.get_notes_end_after_now()} </b>із зупинки "{await db_con.get_departure_point_3()}"\n
&#x1F4C5 <b>Дні курсування</b>: {await db_con.get_days()}"""
                                )
        else:
            await db_con.get_and_update_clicks(bus_name)
            message_text = (f"""
&#128652; Ви обрали маршрут #<b>{callback_query.data.split("_")[1]}</b>\n
Автобус було відправлено:
<b>{await db_con.get_departure_time_before_now_1()} {await db_con.get_notes_left_before_now()} </b>із зупинки "{await db_con.get_departure_point_1()}"
<b>{await db_con.get_departure_time_before_now_2()} {await db_con.get_notes_right_before_now()} </b>із зупинки "{await db_con.get_departure_point_2()}"\n
Наступний автобус відправляється:
<b>{await db_con.get_departure_time_after_now_1()} {await db_con.get_notes_left_after_now()} </b>із зупинки "{await db_con.get_departure_point_1()}"
<b>{await db_con.get_departure_time_after_now_2()} {await db_con.get_notes_right_after_now()} </b>із зупинки "{await db_con.get_departure_point_2()}"\n
&#x1F4C5 <b>Дні курсування</b>: {await db_con.get_days()}"""
                                )
        route_google_maps = keyboards.dict_of_buttons[callback_query.data][1]
        await callback_query.message.answer(text=f'<a href="{route_google_maps}">&#128506 Маршрут автобуса на карті</a>')
        await callback_query.message.answer(text=message_text,
                                            reply_markup=await keyboards.bus_keyboard())
    finally:
        await callback_query.answer()
    


