from helper.excel_helper import ExcelHelper
from helper.model import Navigation, Room

def init():
    create_rooms()

def create_rooms():
    helper = ExcelHelper()
    list = helper.read_excel('Einstellungen', 'room')
    rooms = list[0]
    rooms = rooms.reset_index()

    for index, row in rooms.iterrows():
        room_name = row['Raum']
        room = Room(room_name, row['Min'], row['Max'])
        room_id = room.add_to_db()
        if room_id:
            print('Room ' + room_name + 'successfully added')
            nav_item_id = add_navigation_item(room_name)
            if nav_item_id:
                print('navigation item ' + room_name + ' successfully added')
            else:
                print('Could not add navigation item ' + room_name)   
        else:
            print('Could not add room ' + room_name)
        
def add_navigation_item(room_name):
    nav_item = Navigation(text=room_name)
    
    return nav_item.add_to_db()


if __name__ == '__main__':
    init()