from helper.db_helper import DatabaseHelper
from helper.excel_helper import ExcelHelper
from helper.model import Component, GroupAddress, NavItem, Room


class Visualisation():

    def __init__(self) -> None:
        self.excel_helper = ExcelHelper()
        self.db_helper = DatabaseHelper()

    def init_configuration(self):
        self.save_rooms()
        self.save_components()
        self.save_group_addresses()

    def save_rooms(self):
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

    def save_components(self):
        ## read and save components
        self.db_helper.clear_table('component')

        components = self.excel_helper.read_table('Komponenten', 'component')[0]
        components = components.reset_index()

        for index, row in components.iterrows():
            component_name = row['Name']
            component = Component(name=component_name, area=row['Bereich'], room=row['Raum'], category=row['Kategorie'])
            comp_id = component.add_to_db()
            if comp_id:
                print('Component {0} successfully added'.format(component_name))
            else:
                print('Could not add component ' + component_name)


    def save_group_addresses(self):
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

    def create_card_page(self):
        pass


    def create_navigation_bar(self):
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
                self.add_navigation_item(room_name)
            else:
                print('Could not add room ' + room_name)
            
    def add_navigation_item(self, item_name) -> None:
        nav_item = NavItem(text=item_name)
        nav_item_id = nav_item.add_to_db()
        if nav_item_id:
            print('navigation item ' + item_name + ' successfully added')
        else:
            print('Could not add navigation item ' + item_name)   