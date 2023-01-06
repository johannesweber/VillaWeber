from helper.db_helper import DatabaseHelper
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