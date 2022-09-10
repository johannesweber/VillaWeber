from helper.dashboard import Dashboard
from helper.model import NavigationBar

def test_nav_bar():
    nav_bar = NavigationBar()
    nav_bar.fetch_nav_items()

    items = nav_bar.get_items()

    print(items)

def test_dashboard():
    dashboard = Dashboard()
    dashboard.init_configuration()

if __name__ == '__main__':
    test_dashboard()
    