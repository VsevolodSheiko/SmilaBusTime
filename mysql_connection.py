import asyncio
from sqlalchemy import Column, Integer, BigInteger, String, Date, Time, select, delete, update, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from decouple import config
from datetime import datetime


DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_NAME = config("DATABASE_NAME")
DATABASE_URL = "mysql+aiomysql://%s:%s@%s/%s" % ('root', DATABASE_PASSWORD, 'localhost', DATABASE_NAME)


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

route_name = "route_30"


all_users_ids = []


class Clicker(Base):
    __tablename__ = "click_counter"

    route_name = Column(String(length=255), nullable=True, primary_key=True)
    clicks = Column(Integer, nullable=True)
        

class User(Base):
    __tablename__ = "userbase"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(length=255), nullable=True)
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)
    date = Column(Date)
    location = Column(String(length=255), nullable=True)


async def create_bus_class(table_name):
    class Bus(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}
        
        id = Column(Integer, primary_key=True)
        departure_time = Column(Time, nullable=True)
        notes_left = Column(String(length=255), nullable=True)
        departure_time_2 = Column(Time, nullable=True)
        notes_right = Column(String(length=255), nullable=True)
        departure_time_3 = Column(Time, nullable=True)
        notes_end = Column(String(length=255), nullable=True)
        departure_point_1 = Column(String(length=255), nullable=True)
        departure_point_2 = Column(String(length=255), nullable=True)
        departure_point_3 = Column(String(length=255), nullable=True)
        days = Column(String(length=255), nullable=True)

    return Bus
    

async def get_departure_time_before_now_1():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
            stmt = select(bus).where(bus.departure_time <= time_modifier).order_by(bus.departure_time.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time)[:5] if data is not None else "--:--"
            
            return data 


async def get_departure_time_before_now_2():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
            stmt = select(bus).where(bus.departure_time_2 <= time_modifier).order_by(bus.departure_time_2.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time_2)[:5] if data is not None else "--:--"
            
            return data


async def get_departure_time_before_now_3():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
            stmt = select(bus).where(bus.departure_time_3 <= time_modifier).order_by(bus.departure_time_3.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time_3)[:5] if data is not None else "--:--"
            
            return data


async def get_departure_time_after_now_1():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
            stmt = select(bus).where(bus.departure_time >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time)[:5] if data is not None else "--:--"
            
            return data


async def get_departure_time_after_now_2():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time_2 >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time_2)[:5] if data is not None else "--:--"
            
            return data


async def get_departure_time_after_now_3():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
            
            stmt = select(bus).where(bus.departure_time_3 >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = str(data.departure_time_3)[:5] if data is not None else "--:--"
            
            return data


async def get_notes_left_before_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time <= time_modifier).order_by(bus.departure_time.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_left if data is not None else ""
            
            return data


async def get_notes_left_after_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_left if data is not None else ""
            
            return data


async def get_notes_right_before_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time_2 <= time_modifier).order_by(bus.departure_time_2.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_right if data is not None else ""
            
            return data


async def get_notes_right_after_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time_2 >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_right if data is not None else ""
            
            return data


async def get_notes_end_before_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time_3 <= time_modifier).order_by(bus.departure_time_3.desc())
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_end if data is not None else ""
            
            return data


async def get_notes_end_after_now():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            time_modifier = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

            stmt = select(bus).where(bus.departure_time_3 >= time_modifier)
            result = await session.execute(stmt)
            data = result.scalars().first()
            data = data.notes_end if data is not None else ""
            
            return data


async def get_departure_point_1():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            stmt = select(bus.departure_point_1)
            result = await session.execute(stmt)
            data = result.scalars().first()
            
            return data



async def get_departure_point_2():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            stmt = select(bus.departure_point_2)
            result = await session.execute(stmt)
            data = result.scalars().first()
            
            return data


async def get_departure_point_3():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            stmt = select(bus.departure_point_3)
            result = await session.execute(stmt)
            data = result.scalars().first()
            
            return data


async def get_full_departure_time_1():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            
            stmt = select(bus).order_by(bus.departure_time)
            result = await session.execute(stmt)
            data = result.scalars().all()
            data = [value for value in data]
            clear_empty_strings = [value for value in data if value is not None]
            
            full_time_list = []
            for row in clear_empty_strings:
                if len(str(row.notes_left)) > 0 and row.departure_time is not None:
                    to_list = f"{row.departure_time.strftime('%H').zfill(2)}:{row.departure_time.strftime('%M').zfill(2)}{row.notes_left}"
                    full_time_list.append(to_list)
                elif len(str(row.notes_left)) <= 0 and row.departure_time is not None:
                    to_list = f"{row.departure_time.strftime('%H').zfill(2)}:{row.departure_time.strftime('%M').zfill(2)}"
                    full_time_list.append(to_list)
            result = " | ".join(full_time_list)
            return result
        
            
async def get_full_departure_time_2():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            
            stmt = select(bus).order_by(bus.departure_time_2)
            result = await session.execute(stmt)
            data = result.scalars().all()
            data = [value for value in data]
            clear_empty_strings = [value for value in data if value is not None]
            full_time_list = []
            for row in clear_empty_strings:
                print(row.departure_time_2)
                if len(str(row.notes_right)) > 0 and row.departure_time_2 is not None:
                    to_list = f"{row.departure_time_2.strftime('%H').zfill(2)}:{row.departure_time_2.strftime('%M').zfill(2)}{row.notes_right}"
                    full_time_list.append(to_list)
                elif len(str(row.notes_right)) <= 0 and row.departure_time_2 is not None:
                    to_list = f"{row.departure_time_2.strftime('%H').zfill(2)}:{row.departure_time_2.strftime('%M').zfill(2)}"
                    full_time_list.append(to_list)
            result = " | ".join(full_time_list)
            return result


async def get_full_departure_time_3():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():

            stmt = select(bus).order_by(bus.departure_time_3)
            result = await session.execute(stmt)
            data = result.scalars().all()
            data = [value for value in data]
            clear_empty_strings = [value for value in data if value is not None]
            full_time_list = []
            for row in clear_empty_strings:
                if len(str(row.notes_end)) > 0 and row.departure_time_3 is not None:
                    to_list = f"{row.departure_time_3.strftime('%H').zfill(2)}:{row.departure_time_3.strftime('%M').zfill(2)}{row.notes_end}"
                    full_time_list.append(to_list)
                elif len(str(row.notes_end)) <= 0 and row.departure_time_3 is not None:
                    to_list = f"{row.departure_time_3.strftime('%H').zfill(2)}:{row.departure_time_3.strftime('%M').zfill(2)}"
                    full_time_list.append(to_list)
            result = " | ".join(full_time_list)
            return result


async def insert_new_user(telegram_id, username, first_name, last_name, date, location=None):
    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add(
                User(
                    telegram_id=telegram_id,
                    username=username, 
                    first_name=first_name,
                    last_name=last_name,
                    date=date,
                    location=location)
                )
            await session.commit()


async def update_date_existing_user(telegram_id, date):
    async with AsyncSession(engine) as session:
        async with session.begin():
            stmt = update(User).where(User.telegram_id == telegram_id).values(date=date)
            await session.execute(stmt)


async def delete_user(user_telegram_id):
    async with AsyncSession(engine) as session:
        async with session.begin():
            stmt = delete(User).where(User.telegram_id == user_telegram_id)
            await session.execute(stmt)


async def get_days():
    global route_name
    bus = await create_bus_class(route_name)
    async with AsyncSession(engine) as session:
        async with session.begin():
            stmt = select(bus.days)
            result = await session.execute(stmt)
            data = result.scalars().first()
            return data


async def get_and_update_clicks(bus_name):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Clicker).where(Clicker.route_name == bus_name))
            data = result.scalars().first()
            data = data.clicks + 1
            stmt = update(Clicker).where(Clicker.route_name == bus_name).values(clicks=data)
            await session.execute(stmt)


async def set_clickers_to_zero():
    async with AsyncSession(engine) as session:
        async with session.begin():
            stmt = select(Clicker.route_name)
            result = await session.execute(stmt)
            data = result.scalars().all()
            for i in data:
                stmt = update(Clicker).where(Clicker.route_name == i).values(clicks = 0)
                await session.execute(stmt)


async def get_clicks_count():
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Clicker))
            data = result.scalars().all()
            temp = {i.route_name:i.clicks for i in data}
            return temp


async def get_all_users_ids() -> None:
    async with AsyncSession(engine) as session:
        async with session.begin():
            global all_users_ids

            all_users_ids.clear()
            result = await session.execute(select(User.telegram_id))
            data = result.scalars().all()
            for telegram_id in data:
                all_users_ids.append(telegram_id)
            if len(all_users_ids) != 0:
                all_users_ids = [set(all_users_ids)][0]
            all_users_ids = list(all_users_ids)
            print(all_users_ids)


async def update_location(message, location_global):
    async with AsyncSession(engine) as session:
        async with session.begin():

            stmt = update(User).where(User.telegram_id == message.from_user.id).values(location=f"{location_global.latitude} {location_global.longitude}")
            result = await session.execute(stmt)
