from helper.db_helper import DatabaseHelper
from helper.init_db import RoomTable, ComponentTable, GroupAddressTable, CategoryTemplateTable, PageComponentTable

class PageComponent(PageComponentTable):

    db_helper = None

    def __init__(self, page, component_id, order=99) -> None:
        super().__init__()
        self.page = page
        self.component_id = component_id
        self.order = order
        self.db_helper = DatabaseHelper()

    def add_to_db(self) -> int:
        return self.db_helper.add(self)

class CategoryTemplate(CategoryTemplateTable):

    db_helper = None

    def __init__(self, ) -> None:
        super().__init__()
        self.db_helper = DatabaseHelper()

    def create(self, category, template) -> int:
        self.category = category
        self.template = template

        return self.db_helper.add(self)

class Component(ComponentTable):

    db_helper = None

    def __init__(self) -> None:
        super().__init__()
        self.db_helper = DatabaseHelper()

    def create(self, area, room, category, name, is_favourite=False) -> int:
        if name is None:
            self.name = ''
        else:
            self.name = name
        self.area = area
        self.room = room
        self.category = category
        self.is_favorite = is_favourite

        return self.db_helper.add(self)

    def fetch_from_db(self, room_name):
        self.items = self.db_helper.fetch_entity_where(class_name='Component', room=room_name)


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

        try:
            self.main_group = int(groups[0])
        except:
            self.main_group = None

        try:
            self.middle_group = int(groups[1])
        except:
            self.middle_group = None

        try:
            self.under_group = int(groups[2])
        except:
            self.under_group = None

    def add_to_db(self) -> int:
        return self.db_helper.add(self)

    def has_under_group(self) -> bool:
        if self.under_group is None:
            return False
        else:
            return True


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