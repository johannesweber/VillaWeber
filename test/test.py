from helper.visualisation import Visualisation
from helper.model import NavigationBar

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
    