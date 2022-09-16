from helper.db_helper import DatabaseHelper
from helper.excel_helper import ExcelHelper
from villaweber.model.navigation import NavigationBar, NavItem
from villaweber.model.database import Component, Room, GroupAddress, CategoryTemplate
from villaweber.model.page import Page


class Visualisation():

    navigation_bar = None
    pages = None

    def __init__(self) -> None:
        self.excel_helper = ExcelHelper()
        self.db_helper = DatabaseHelper()
        self.navigation_bar = NavigationBar()
        self.pages = {} #dictionary with 'page_name': 'Page Object'

    def init_configuration(self) -> None:
        # read and save excel file
        self._save_rooms()
        self._save_components()
        self._save_group_addresses()

        #populate db with default entries
        self._save_navigation_bar_db()
        self._save_templates_db()
        self._save_page_components_db()

    def get_page(self, page_name) -> Page:
        return self.pages[page_name]

    def get_pages(self) -> list:
        return self.pages

    def get_navigation_bar(self) -> NavigationBar:
        return self.navigation_bar

    def build() -> None:
        pass # Build up the whole visualisation

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
                print('Room ' + room_name + ' successfully added')
            else:
                print('Could not add room ' + room_name)

    def _save_components(self):
        ## read and save components
        self.db_helper.clear_table('component')

        components = self.excel_helper.read_table('Komponenten', 'component')[0]
        components = components.reset_index()

        for index, row in components.iterrows():
            component_name = row['Name']
            component = Component()
            comp_id = component.create(name=component_name, area=row['Bereich'], room=row['Raum'], category=row['Kategorie'])
            if comp_id:
                print('Component {0} successfully added'.format(component_name))
            else:
                print('Could not add component ' + component_name)


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
                    print('Group address ' + group_address_name + ' successfully added')
                else:
                    print('Could not add Group address ' + group_address_name)

    def _save_templates_db(self):
        category_template = CategoryTemplate()
        category_template.create(category = 'Licht', template = 'light')

    def _save_page_components_db(self):
        # read navigation items
        # read components with room filter (=navigation item name)
        # populate PageComponentTable (page=navigation target, component_id = compoenent.id)
        pass

    def _save_navigation_bar_db(self):
        # read rooms from db and save as navigation item in db
        list = self.excel_helper.read_table('Einstellungen', 'room')
        rooms = list[0]
        rooms = rooms.reset_index()

        self.add_navigation_item('Dashboard')

        for index, row in rooms.iterrows():
            room_name = row['Raum']
            room = Room(room_name, row['Min'], row['Max'])
            room_id = room.add_to_db()
            if room_id:
                print('Room ' + room_name + ' successfully added')
                self._save_navigation_item(room_name)
            else:
                print('Could not add room ' + room_name)
            
    def _save_navigation_item(self, item_name) -> None:
        nav_item = NavItem(text=item_name)
        nav_item_id = nav_item.add_to_db()
        if nav_item_id:
            print('navigation item ' + item_name + ' successfully added')
        else:
            print('Could not add navigation item ' + item_name)   