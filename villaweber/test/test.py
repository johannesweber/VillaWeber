from helper.model import NavigationBar
from visualisation import Visualisation

def test_nav_bar():
    nav_bar = NavigationBar()
    nav_bar.fetch_nav_items()

    items = nav_bar.get_items()

    print(items)

def test_visu():
    visu = Visualisation()
    visu.init_configuration()

if __name__ == '__main__':
    test_visu()
    