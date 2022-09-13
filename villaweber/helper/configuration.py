#!/usr/bin/env python
import configparser
from helper import util


class Configuration:

    def __init__(self, file_name):
        self.fritzbox_user = None
        self.fritzbox_pw = None
        self.fritzbox_ip = None
        self.residents = None

        config_path = util.get_path('config')
        final_path = config_path + file_name + '.cfg'

        self._config = configparser.ConfigParser()
        self._config.read(final_path)

    def load(self):
        self.fritzbox_user = self.get_value('fritzbox', 'user')
        self.fritzbox_pw = self.get_value('fritzbox', 'pw')
        self.fritzbox_ip = self.get_value('fritzbox', 'ip')
        self.residents = self.get_list('fritzbox', 'residents')
        self.ga_excel_path = self.get_value('knx', 'ga_excel_path')

    def get_boolean_value(self, group, attribute):
        return util.string_2_bool(self.get_value(group, attribute))

    def get_integer_value(self, group, attribute):
        integer_value = self.get_value(group, attribute)
        return int(integer_value)

    def get_list(self, section, field_name):
        values = self.get_value(section, field_name)
        return self._values_to_list(values)

    def get_value(self, group, attribute):
        try:
            result = self._config[group][attribute]
            if not result:
                result = None
        except KeyError:
            result = None
        return result

    def get_section(self, section_name):
        try:
            result = self._config[section_name]
        except KeyError:
            result = None
        return result

    @staticmethod
    def _values_to_list(values):
        if values:
            tables_list = [value.strip() for value in values.split(",")]
        else:
            tables_list = []
        return tables_list
