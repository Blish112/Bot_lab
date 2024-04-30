import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import datetime

from sqlalchemy import BigInteger, Integer, Boolean, Date, ForeignKey, Identity, Time
from sqlalchemy.engine import URL
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from data.config_reader import drivername, username, password, database, host, port

url_postgresql = URL.create(
    drivername=drivername,
    username=username,
    password=password,
    database=database,
    host=host,
    port=port
)

url_postgresql_sync = URL.create(
    drivername="postgresql",
    username=username,
    password=password,
    database=database,
    host=host,
    port=port
)

engine = create_async_engine(url=url_postgresql, echo=True)
ansyc_ssesion = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

# Описание талицы пользователя
class User(Base):
    __tablename__ = 'users'
    
    # id from telegram - primary_key
    tg_id = mapped_column(BigInteger, Identity(), primary_key=True)
    
    # name from telegram 
    fullname: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column()
    
    # default var 
    is_baned = mapped_column(Boolean, nullable=False, default=False)
    is_accept = mapped_column(Boolean, nullable=False, default=False)
    try_to_accept: Mapped[int] = mapped_column(nullable=False, default=3)
    
    # num_of_group <- after registration 
    id_group: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True, default=None)
    group = relationship('Group', back_populates='user')
    
    # registration date and date last using
    reg_date = mapped_column(Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    upd_date = mapped_column(Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    
# Описание талицы группы
class Group(Base):
    __tablename__ = 'groups'
    
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    
    # Имя группы
    name_group: Mapped[str] = mapped_column(unique=True)
    
    # Кафедра
    id_departure: Mapped[int] = mapped_column(ForeignKey('departures.id'), nullable=False)
    departure = relationship('Departure', back_populates='group')
    
    # направление подготовки
    id_program: Mapped[int] = mapped_column(ForeignKey('programs.id'), nullable=False)
    program = relationship('Program', back_populates='group')
    
    # relationships
    classe = relationship('Class', back_populates='group')
    user = relationship('User', back_populates='group')

# Описание талицы направления подготовки
class Program(Base):
    __tablename__ = 'programs'
    
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    
    # Название направления подготовки
    program_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    # Бакалавриат/Магистратура/Специалитет/Аспирантура
    degree: Mapped[str] = mapped_column(unique=False, nullable=False)
    
    # relationships
    group = relationship('Group', back_populates='program')
    

class Departure(Base):
    __tablename__ = 'departures'
    
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    
    # Название кафедры
    departure_name: Mapped[str] = mapped_column(unique=False, nullable=False)
    
    # Название иститута
    institute_name: Mapped[str] = mapped_column(unique=False, nullable=False)
    
    # Бакалавриат/Магистратура/Специалитет/Аспирантура
    departure_number: Mapped[int] = mapped_column(unique=False, nullable=False)
    
    # relationships
    group = relationship('Group', back_populates='departure')

# Описание талицы числ/знам
class Numerator(Base):
    __tablename__ = 'numerator'
    
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    what_is_now = mapped_column(Boolean, nullable=False)

# Описание талицы строение
class Building(Base):
    __tablename__ = 'buildings'
    
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    building_name: Mapped[str] = mapped_column(unique=True)
    
    shedule = relationship('Schedule', back_populates='building')

# Описание талицы звонки
class Schedule(Base):
    __tablename__ = 'shedules'
    
    # id from telegram - primary_key
    id = mapped_column(Integer, Identity(), primary_key=True)
    
    # номер пары
    class_number: Mapped[int] = mapped_column()
    
    # время начала и конца
    start_time = mapped_column(Time)
    end_time = mapped_column(Time)
    
    # корпус
    id_building: Mapped[int] = mapped_column(ForeignKey('buildings.id'), nullable=False)
    building = relationship('Building', back_populates='shedule')
    
    # relationships
    classe = relationship('Class', back_populates='shedule')


# Описание талицы дисциплины
class Subject(Base):
    __tablename__ = 'subjects'
    
    # id - primary_key
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True, unique=True)
    
    # name subject 
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    # format - online (True) / offline (False) 
    format: Mapped[bool] = mapped_column(nullable=False)
    
    # moodle_link 
    moodle_link: Mapped[str] = mapped_column(nullable=True)
    second_link: Mapped[str] = mapped_column(nullable=True, default=None)
    
    # Номер кабинета - существует если пара оффлайн / отсутсвует если пара онлайн (учитывать при заполнении)  
    class_addresses: Mapped[str] = mapped_column(nullable=True, default=None)
    
    # relationships
    classe = relationship('Class', back_populates='subject')


# Описание таблицы пары
class Class(Base):
    __tablename__ = 'classes'
    
    # id - primary_key
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True, unique=True)
    
    # День недели
    weekday: Mapped[int] = mapped_column()
    
    # номер пары
    class_number: Mapped[int] = mapped_column()
    
    # числ/знам
    numerator: Mapped[bool] = mapped_column(nullable=True, unique=False)
    
    # Предмет
    id_subject: Mapped[int] = mapped_column(ForeignKey('subjects.id'), nullable=False)
    subject = relationship('Subject', back_populates='classe')
    
    # Время
    id_schedule: Mapped[int] = mapped_column(ForeignKey('shedules.id'), nullable=False)
    shedule = relationship('Schedule', back_populates='classe')
    
    # Группа
    id_group: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', back_populates='classe')
    

# Создание таблиц
async def async_upd_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)