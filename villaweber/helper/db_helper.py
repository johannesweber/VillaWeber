from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import constants
from helper import util

import logging


class DatabaseHelper:
    logger = logging.getLogger(__name__)
    connection = None
    session = None
    meta = None

    def __init__(self):
        root_path = util.get_path('data')
        final_path = str(root_path + constants.DB_NAME)
        self.logger.info('Database Path: {0}'.format(final_path))
        self.connection = create_engine('sqlite:///' + final_path)
        self.meta = MetaData(bind=self.connection)
        self.meta.reflect()

        self.create_session()

    def get_connection(self):
        return self.connection

    def create_session(self):
        db_session = sessionmaker(bind=self.connection)
        self.session = db_session()

    def add(self, database_entity):
        self.session.add(database_entity)
        self.session.commit()
        self.session.flush()
        return database_entity.id

    def delete(self, database_entity):
        self.session.delete(database_entity)
        self.session.commit()

    def update(self, database_entity):
        entity = self.session.merge(database_entity)
        self.commit()
        return entity

    def commit(self):
        self.session.commit()

    def insert_all(self, entries):
        self.session.add_all(entries)
        self.commit()

    def fetch_entity_where(self, class_name, fetch_all=True, negated=False, **kwargs):
        self.logger.info('Fetching Enitity {0} from SQLite3'.format(class_name))
        try:
            mod = __import__('helper.model', fromlist=[class_name])
            entity_class = getattr(mod, class_name)
        except AttributeError:
            mod = __import__('helper.init_db', fromlist=[class_name])
            entity_class = getattr(mod, class_name)
        query = self.session.query(entity_class)
        if kwargs is not None:
            for key, value in kwargs.items():
                attribute = getattr(entity_class, key)
                if negated:
                    query = query.filter(attribute != value)
                else:
                    query = query.filter(attribute == value)

        if fetch_all:
            result = query.all()
        else:
            result = query.first()
        return result

    def close_session(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def clear_all(self):
        self.connection.execute('PRAGMA foreign_keys = OFF')
        for table in self.meta.sorted_tables:
            name = table.name
            if name != 'setting':
                self.connection.execute(table.delete())
        self.connection.execute('PRAGMA foreign_keys = ON')

    def clear_table(self, table_name):
        self.connection.execute('PRAGMA foreign_keys = OFF')
        for table in self.meta.sorted_tables:
            name = table.name
            if name == table_name:
                self.connection.execute(table.delete())
        self.connection.execute('PRAGMA foreign_keys = ON')
