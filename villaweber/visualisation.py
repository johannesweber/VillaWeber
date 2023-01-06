import pandas as pd

from helper.db_helper import DatabaseHelper
from helper.excel_helper import ExcelHelper
from model.database import (CategoryTemplate, Component, GroupAddress, NavItem,
                            PageComponent, Room)
from model.navigation import NavigationBar
from model.page import Page
import helper.util as util
from collections import defaultdict

class Visualisation():

    logger = None

    excel_helper = None
    db_helper = None

    navigation_bar = None
    pages = None

    room_buffer = None
    nav_item_buffer = None
    components_buffer = None

    def __init__(self, logger) -> None:
        self.logger = logger

        self.excel_helper = ExcelHelper()
        self.db_helper = DatabaseHelper()
        
        self.navigation_bar = NavigationBar()
        self.pages = defaultdict() #dictionary with 'page_name': 'Page Object'
        
        # buffer with data from database 
        self.room_buffer = []
        self.nav_item_buffer = []
        # buffer with data from excel file
        self.components_buffer = pd.DataFrame()
        
    def init_configuration(self) -> None:
        self._save_excel_file()

        # populate db with default entries
        self._save_navigation_bar_db()
        self._save_templates_db()
        self._save_page_components_db()
        # ToDo:
        # save dashboard components; is every component marked as favourite 

    def _save_excel_file(self) -> None:
        # read and save excel file
        self._save_rooms()
        self._save_components()
        self._save_group_addresses()

    def set_logger(self, logger):
        self.logger = logger

    def get_page(self, page_name) -> Page:
        return self.pages[page_name]

    def get_pages(self) -> defaultdict:
        return self.pages

    def build_navigation_bar(self) -> bool:
        success = False
        self.navigation_bar.fetch_nav_items()
        if self.navigation_bar.get_items():
            success = True
        return success

    def get_navigation_bar(self) -> NavigationBar:
        self.navigation_bar.fetch_nav_items()
        return self.navigation_bar.get_items()

    def build_page(self, page_name) -> bool:
        page = Page(page_name)
        success = page.load()
        if success:
            self.pages[page_name] = page
        return success


### Save excel data for initialization to database and create default data ###

    def _save_rooms(self):
        ## read rooms
        self.db_helper.clear_table('room')

        rooms = self.excel_helper.read_table('Einstellungen', 'room')[0]
        rooms = rooms.reset_index()

        ## save rooms
        for index, row in rooms.iterrows():
            room_name = row['Raum']
            room = Room(room_name, row['Min'], row['Max'])
            room_id = room.add_to_db()
            if room_id:
                self.logger.info('Room ' + room_name + ' successfully added')
                self.room_buffer.append(room)
            else:
                self.logger.error('Could not add room ' + room_name)

    def _save_components(self):
        ## read and save components
        self.db_helper.clear_table('component')

        components = self.excel_helper.read_table('Komponenten', 'component')[0]
        components = components.reset_index()
        self.components_buffer = components

        for index, row in components.iterrows():
            component_name = row['Name']
            component = Component()
            comp_id = component.create(name=component_name, area=row['Bereich'], room=row['Raum'], category=row['Kategorie'])
            if comp_id:
                self.logger.info('Component {0} successfully added'.format(component_name))
            else:
                self.logger.error('Could not add component ' + component_name)


    def _save_group_addresses(self):
        ## read and save group addresses
        self.db_helper.clear_table('group_address')

        addresses = self.excel_helper.read_table('Gruppenadressen')[0]
        addresses = addresses.reset_index()

        for index, row in addresses.iterrows():
            group_address_name = row['Group name']
            group_address = GroupAddress(name=group_address_name,address=row['Address'], datapoint=row['DatapointType'], description=row['Description'])
            if group_address.has_under_group():
                ga_id = group_address.add_to_db()
                if ga_id:
                    self.logger.info('Group address ' + group_address_name + ' successfully added')
                else:
                    self.logger.error('Could not add Group address ' + group_address_name)

    def _save_templates_db(self):
        self.db_helper.clear_table('category_template')

        category_template = CategoryTemplate()
        category_template.create(category = 'Licht', template = 'light')
        # Todo: weitere Templates mit aufnehmen wenn das Licht Template funktioniert

    def _save_page_components_db(self):
        self.db_helper.clear_table('page_component')

        if not self.nav_item_buffer:
            self.nav_item_buffer = self.db_helper.fetch_entity_where(class_name="NavItem")

        if self.components_buffer.empty:
                    components = self.excel_helper.read_table('Komponenten', 'component')[0]
                    components = components.reset_index()
                    self.components_buffer = components

        for item in self.nav_item_buffer:
            filtered_components = self.components_buffer.loc[self.components_buffer.Raum == item.text]
            for index, component in filtered_components.iterrows():
                if component.Name:
                    component_db = self.db_helper.fetch_entity_where(class_name="Component", fetch_all=True, negated=False, area=component.Bereich, room=component.Raum, category=component.Kategorie, name=component.Name)[0]
                else:
                    component_db = self.db_helper.fetch_entity_where(class_name="Component", fetch_all=True, negated=False, area=component.Bereich, room=component.Raum, category=component.Kategorie)[0]
                page_component = PageComponent(page=item.target, component_id=component_db.id)
                page_componet_id = page_component.add_to_db()
                if page_componet_id:
                    self.logger.info('Component ' + component_db.name + ' for Page ' + item.text + ' successfully added')
                else:
                    self.logger.error('Could not add Component ' + component_db.name + ' for Page ' + item.text)
        pass

    def _save_navigation_bar_db(self):
        self.db_helper.clear_table('navigation')
        # read rooms from buffer and save as navigation item in db
        self._save_navigation_item(text='Dashboard', target='dashboard')

        for room in self.room_buffer:
            escaped_name = util.replace_umlaute(room.name)
            self._save_navigation_item(text=room.name, target=escaped_name.lower())
            
    def _save_navigation_item(self, text, target) -> None:
        nav_item = NavItem(text=text, target=target)
        nav_item_id = nav_item.add_to_db()
        if nav_item_id:
            self.logger.info('navigation item ' + text + ' successfully added')
            self.nav_item_buffer.append(nav_item)
        else:
            self.logger.error('Could not add navigation item ' + text)   
