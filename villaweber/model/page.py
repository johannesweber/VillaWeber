from model.database import Component
from helper.db_helper import DatabaseHelper
from collections import OrderedDict, defaultdict
import helper.util as util

class Group():

    title = None # component category
    name = None # category title in lower case and replaced umlaute
    components = None # components ordered by order number

    def __init__(self, title, name) -> None:
        self.components = []
        self.title = title
        self.name = name

    def add_component(self, component: Component):
        self.components.append(component)

class Page():

    title = None
    name = None
    groups = None # component category in our case
    db_helper = None

    def __init__(self, name) -> None:
        self.groups = {}
        self.name = name
        self.db_helper = DatabaseHelper()

    def load(self) -> bool:
        success = True
        title = self.load_title(self.name)
        if not title:
            success = False
        else:
            self.title = title

        groups = self.build_groups(self.name)
        if not groups:
            success = False
        else:
            self.groups = groups

        return success

    def add_group(self, group: Group) -> None:
        self.groups[group.title] = group

    def build_groups(self, page_name) -> defaultdict:
        groups = defaultdict(list)
        page_component_db = self.db_helper.fetch_entity_where(class_name='PageComponent', fetch_all=True, negated=False, order_by=['order'], page=page_name)
        for item in page_component_db:
            component = self.load_component(item.component_id)
            group_title = component.category
            group_name = util.replace_umlaute(group_title).lower()
            group = Group(title=group_title, name=group_name)
            group.add_component(component=component)
            groups[group_name].append(component)
        return groups

    def load_title(self, page_name) -> str:
        title = None
        db_entity = self.db_helper.fetch_entity_where(class_name='NavItem', fetch_all=False, negated=False, target=page_name)
        if db_entity:
            title = db_entity.text
        return title

    def load_component(self, id) -> Component:
        result = None
        db_entity = self.db_helper.fetch_entity_where(class_name='Component', fetch_all=False, negated=False, id=id)
        if db_entity:
            result = db_entity
        return result

