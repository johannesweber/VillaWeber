#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, create_engine, MetaData, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from config import constants
import logging

Base = declarative_base()

class StatisticsType(enum.Enum):
    LIGHT = 1
    BLINDS = 2
    WIND = 3
    BRIGHTNESS = 4
    TEMPERATURE = 5
    SCENES = 6
    SOCKET = 7


class Unit(enum.Enum):
    KMH = 1
    CELSIUS = 2
    LUX = 3


class RoomTable(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)


class ComponentTable(Base):
    __tablename__ = 'component'

    id = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(String, nullable=False)
    room = Column(String, ForeignKey('room.name'), nullable=False)
    category = Column(String, nullable=False)
    name = Column(String)
    is_favorite = Column(Boolean)


class GroupAddressTable(Base):
    __tablename__ = 'group_address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    main_group = Column(Integer, nullable=False)
    middle_group = Column(Integer, nullable=False)
    under_group = Column(Integer, nullable=False)
    datapoint = Column(String)
    description = Column(String)


class CategoryTemplateTable(Base):
    __tablename__ = 'category_template'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, ForeignKey('component.category'), nullable = False)
    template = Column(String, nullable=False)


class ElementNameMappingTable(Base):
    __tablename__ = 'element_name_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    element_name = Column(String, nullable=False)
    ga_name_substring = Column(String, nullable=False)


class PageComponentTable(Base):
    __tablename__ = 'page_component'

    id = Column(Integer, primary_key=True, autoincrement=True)
    page = Column(String, ForeignKey('navigation.target'), nullable=False)
    component_id = Column(Integer, ForeignKey('component.id'), nullable=False)
    order = Column(Integer)


class NavigationTable(Base):
    __tablename__ = 'navigation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    target = Column(String, nullable=False)
    html_file = Column(String)
    mode = Column(String)
    order = Column(Integer)
    hidden = Column(Boolean)


class MessageTable(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)


class StatisticTable(Base):
    __tablename__ = 'statistic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    statistic_type = Column(Enum(StatisticsType), nullable = False)
    date = Column(DateTime, nullable=False)
    value = Column(Numeric(2), nullable=False)
    unit = Column(Enum(Unit), nullable = False)


class KeyValueTable(Base):
    __tablename__ = 'key_value'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    root_path = Path(__file__).parents[1]
    final_path = str(root_path.joinpath('data/' + constants.DB_NAME))
    logger.info('Database Path: {0}'.format(final_path))
    connection = create_engine('sqlite:///' + final_path)
    meta = MetaData(bind=connection)
    meta.reflect()

    db_session = sessionmaker(bind=connection)
    session = db_session()
    Base.metadata.create_all(connection)