from helper.db_helper import DatabaseHelper
from helper.init_db import NavigationTable, RoomTable

class Navigation(NavigationTable):

    db_helper = DatabaseHelper()

    def __init__(self, text, icon='abc', target='content.html', mode=None, order='99') -> None:
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

