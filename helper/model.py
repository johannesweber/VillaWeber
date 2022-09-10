from helper.db_helper import DatabaseHelper
from helper.init_db import NavigationTable, RoomTable, ComponentTable, GroupAddressTable

class PageContent():

    title = None
    accordion_items = None
    cards = None

    def __init__(self) -> None:
        self.accordion_items = []
        self.cards = []
        self.title = str


class AccordionItem():

    title = None
    cards = None

    def __init__(self, title) -> None:
        self.cards = []
        self.title = title

    def add_card(self, card):
        self.cards.append(card)


class Card():
    
    title = None
    subtitle = None

    def __init__(self, title, subtitle=None) -> None:
        self.title = title
        self.subtitle = subtitle


class Component(ComponentTable):

    db_helper = None

    def __init__(self, area, room, category, name, is_favourite=False) -> None:
        super().__init__()
        self.name = name
        self.area = area
        self.room = room
        self.category = category
        self.is_favorite = is_favourite
        self.db_helper = DatabaseHelper()

    def add_to_db(self) -> int:
        return self.db_helper.add(self)


class GroupAddress(GroupAddressTable):

    db_helper = None

    def __init__(self, address, name, datapoint=None, description=None) -> None:
        super().__init__()
        self.name = name
        self.address = address
        self.datapoint = datapoint
        self.description = description
        self.db_helper = DatabaseHelper()

        groups = address.split('/')
        self.main_group = groups[0]
        self.middle_group = groups[1]
        self.under_group = groups[2]

    def add_to_db(self) -> int:
        return self.db_helper.add(self)

class NavigationBar():

    items = None
    title = None
    db_helper = None

    def __init__(self) -> None:
        self.items = []
        self.title = 'VillaWeber'
        self.db_helper = DatabaseHelper()

    def update_nav_items(self):
        self.items = []
        self.fetch_nav_items()

    def fetch_nav_items(self):
        self.items = self.db_helper.fetch_entity_where(class_name='NavItem')

    def get_items(self) -> list:
        return self.items

    def get_title(self) -> str:
        return self.title


class NavItem(NavigationTable):

    db_helper = DatabaseHelper()

    def __init__(self, text, icon='home', target='content.html', mode=None, order='99') -> None:
        self.icon = icon
        self.text = text
        self.target = target
        self.mode = mode
        self.order = order

    def add_to_db(self) -> int:
        return self.db_helper.add(self)


class Room(RoomTable):

    db_helper = None

    def __init__(self, name, min, max) -> None:
        super().__init__()
        self.name = name
        self.min = min
        self.max = max
        self.db_helper = DatabaseHelper()

    def add_to_db(self) -> int:
        return self.db_helper.add(self)

