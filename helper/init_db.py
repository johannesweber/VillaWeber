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

    room = Column(String, primary_key=True)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)


class ComponentTable(Base):
    __tablename__ = 'component'

    id = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(String, nullable=False)
    room = Column(String, ForeignKey('room.name'), nullable=False)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_favorite = Column(Boolean)

class GroupAddressTable(Base):
    __tablename__ = 'group_address'

    address = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    main_group = Column(Integer, nullable=False)
    middle_group = Column(Integer, nullable=False)
    under_group = Column(Integer, nullable=False)
    datapoint = Column(String)
    description = Column(String)


class CategoryTemplateTable(Base):
    __tablename__ = 'category_template'

    category = Column(String, ForeignKey('component.category'), primary_key=True)
    template = Column(String, nullable=False)
    

class PageTable(Base):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    html_file = Column(String, nullable=False)


class PageComponentTable(Base):
    __tablename__ = 'page_component'

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('page.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('component.id'), nullable=False)

class NavigationTable(Base):
    __tablename__ = 'navigation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    icon = Column(String, nullable=False)
    text = Column(String, nullable=False)
    target = Column(String, nullable=False)
    mode = Column(String)


class TemplateSettingTable(Base):
    __tablename__ = 'template_setting'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    template = Column(String, primary_key=True)
    element_id = Column(String, primary_key=True)
    ga_description = Column(String, nullable=False)
    ga_function = Column(String, nullable=False)


class MessageTable(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)


class StatisticsTable(Base):
    __tablename__ = 'statisctics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    statistic_type = Column(Enum(StatisticsType), nullable = False)
    date = Column(DateTime, nullable=False)
    value = Column(Numeric(2), nullable=False)
    unit = Column(Enum(Unit), nullable = False)


class KeyValueTable(Base):
    __tablename__ = 'key_value'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    root_path = Path(__file__).parents[1]
    final_path = str(root_path.joinpath('config/' + constants.DB_NAME))
    logger.info('Database Path: {0}'.format(final_path))
    connection = create_engine('sqlite:///' + final_path)
    meta = MetaData(bind=connection, reflect=True)

    db_session = sessionmaker(bind=connection)
    session = db_session()
    Base.metadata.create_all(connection)