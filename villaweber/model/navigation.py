from cgitb import html
from helper.db_helper import DatabaseHelper
from helper.init_db import NavigationTable

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

    def __init__(self, text, icon='home', target='content', html_file='content.html', mode=None, order='99', hidden=False) -> None:
        self.icon = icon
        self.text = text
        self.target = target
        self.html_file = html_file
        self.mode = mode
        self.order = order
        self.hidden = hidden

    def add_to_db(self) -> int:
        return self.db_helper.add(self)