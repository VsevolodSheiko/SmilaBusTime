import os

from peewee import *

from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

db = MySQLDatabase(DATABASE_NAME,
                   host='localhost',
                   user='root',
                   password=DATABASE_PASSWORD,
                   port=3306)

route_name = ""

db.connect()
cursor = db.cursor()


class User(Model):
    id = BigIntegerField(primary_key=False, null=True)
    username = CharField(max_length=255, null=True)
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    date = DateField()

    class Meta:
        database = db
        table_name = "userbase"


def process_bus_class(route):
    class Bus(Model):
        id = IntegerField(primary_key=True, null=False)
        departure_time = TimeField(null=True)
        notes_left = CharField(max_length=255, null=True)
        departure_time_2 = TimeField(null=True)
        notes_right = CharField(max_length=255, null=True)
        departure_time_3 = TimeField(null=True)
        notes_end = CharField(max_length=255, null=True)
        departure_point_1 = CharField(max_length=100, null=True)
        departure_point_2 = CharField(max_length=100, null=True)
        departure_point_3 = CharField(max_length=100, null=True)
        days = CharField(max_length=255, null=True)

        class Meta:
            database = db
            table_name = route

    return Bus


def get_departure_time_before_now_1():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().order_by(bus.departure_time.desc()).where(bus.departure_time <= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.departure_time)
    if len(temp) > 0:
        return str(temp[0])[:5]
    else:
        return "--:--"


def get_departure_time_before_now_2():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().order_by(bus.departure_time_2.desc()).where(bus.departure_time_2 <= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.departure_time_2)
    if len(temp) > 0:
        return str(temp[0])[:5]
    else:
        return "--:--"


def get_departure_time_before_now_3():
    bus = process_bus_class(route_name)
    if route_name == "route_3":
        time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        rows = bus.select().order_by(bus.departure_time_3.desc()).where(bus.departure_time_3 <= time_modifier)
        temp = []
        for row in rows:
            temp.append(row.departure_time_3)
        if len(temp) > 0:
            return str(temp[0])[:5]
        else:
            return "--:--"
    else:
        return ""


def get_departure_time_after_now_1():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().where(bus.departure_time >= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.departure_time)
    if len(temp) > 0:
        return str(temp[0])[:5]
    else:
        return "--:--"


def get_departure_time_after_now_2():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().where(bus.departure_time_2 >= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.departure_time_2)
    if len(temp) > 0:
        return str(temp[0])[:5]
    else:
        return "--:--"


def get_departure_time_after_now_3():
    bus = process_bus_class(route_name)
    if route_name == "route_3":
        time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        rows = bus.select().where(bus.departure_time_3 >= time_modifier)
        temp = []
        for row in rows:
            temp.append(row.departure_time_3)
        if len(temp) > 0:
            return str(temp[0])[:5]
        else:
            return "--:--"
    else:
        return ""


def get_notes_left_before_now():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().order_by(bus.departure_time.desc()).where(bus.departure_time <= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.notes_left)
    if len(temp) > 0:
        return temp[0]
    else:
        return ""


def get_notes_right_before_now():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().order_by(bus.departure_time_2.desc()).where(bus.departure_time_2 <= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.notes_right)
    if len(temp) > 0:
        return temp[0]
    else:
        return ""


def get_notes_left_after_now():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().where(bus.departure_time >= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.notes_left)
    if len(temp) > 0:
        return temp[0]
    else:
        return ""


def get_notes_right_after_now():
    bus = process_bus_class(route_name)
    time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

    rows = bus.select().where(bus.departure_time_2 >= time_modifier)
    temp = []
    for row in rows:
        temp.append(row.notes_right)
    if len(temp) > 0:
        return temp[0]
    else:
        return ""


def get_notes_end_before_now():
    bus = process_bus_class(route_name)
    if route_name == "route_3":
        time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        rows = bus.select().order_by(bus.departure_time_3.desc()).where(bus.departure_time_3 <= time_modifier)
        temp = []
        for row in rows:
            temp.append(row.notes_end)
        if len(temp) > 0:
            return temp[0]
        else:
            return ""
    else:
        return ""


def get_notes_end_after_now():
    bus = process_bus_class(route_name)
    if route_name == "route_3":
        time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        rows = bus.select().where(bus.departure_time_3 >= time_modifier)
        temp = []
        for row in rows:
            temp.append(row.notes_end)
        if len(temp) > 0:
            return temp[0]
        else:
            return ""
    else:
        return ""


def get_departure_point_1():
    bus = process_bus_class(route_name)
    rows = bus.select()
    for row in rows:
        return row.departure_point_1


def get_departure_point_2():
    bus = process_bus_class(route_name)
    rows = bus.select()
    for row in rows:
        return row.departure_point_2


def get_departure_point_3():
    bus = process_bus_class(route_name)
    if route_name == "route_3":
        rows = bus.select()
        for row in rows:
            return row.departure_point_3
    else:
        return ""


def get_full_departure_time_1():
    bus = process_bus_class(route_name)
    rows = bus.select()
    full_time_list = []
    for row in rows:
        if len(str(row.notes_left)) > 0 and row.departure_time is not None:
            to_list = f"{row.departure_time.strftime('%H').zfill(2)}:{row.departure_time.strftime('%M').zfill(2)}{row.notes_left}"
            full_time_list.append(to_list)
        elif row.departure_time is None:
            pass
        else:
            to_list = f"{row.departure_time.strftime('%H').zfill(2)}:{row.departure_time.strftime('%M').zfill(2)}"
            full_time_list.append(to_list)
    return full_time_list


def get_full_departure_time_2():
    bus = process_bus_class(route_name)
    rows = bus.select()
    full_time_list = []
    for row in rows:
        if len(str(row.notes_right)) > 0 and row.departure_time_2 is not None:
            to_list = f"{row.departure_time_2.strftime('%H').zfill(2)}:{row.departure_time_2.strftime('%M').zfill(2)}{row.notes_right}"
            full_time_list.append(to_list)
        elif row.departure_time_2 is None:
            pass
        else:
            to_list = f"{row.departure_time_2.strftime('%H').zfill(2)}:{row.departure_time_2.strftime('%M').zfill(2)}"
            full_time_list.append(to_list)
    return full_time_list


def get_full_departure_time_3():
    bus = process_bus_class(route_name)
    rows = bus.select()
    full_time_list = []
    for row in rows:
        if len(str(row.notes_end)) > 0 and row.departure_time_3 is not None:
            to_list = f"{row.departure_time_3.strftime('%H').zfill(2)}:{row.departure_time_3.strftime('%M').zfill(2)}{row.notes_end}"
            full_time_list.append(to_list)
        elif row.departure_time_3 is None:
            pass
        else:
            to_list = f"{row.departure_time_3.strftime('%H').zfill(2)}:{row.departure_time_3.strftime('%M').zfill(2)}"
            full_time_list.append(to_list)
    return full_time_list


def get_days():
    bus = process_bus_class(route_name)
    rows = bus.select()
    for row in rows:
        return row.days
