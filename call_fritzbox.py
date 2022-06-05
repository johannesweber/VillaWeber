import sys
from fritzbox.fritzHelper import FritzHelper

FRITZ = FritzHelper()


def enable_wlan():
    FRITZ.change_wlan_status('on', 'guest', 1)
    FRITZ.change_wlan_status('on', 'guest', 2)
    FRITZ.change_wlan_status('on', 'default')


def disable_wlan():
    FRITZ.change_wlan_status('off', 'guest', 1)
    FRITZ.change_wlan_status('off', 'guest', 2)
    FRITZ.change_wlan_status('off', 'default')


def check_presence():
    return FRITZ.check_presence()


def execute():
    fritz_action = sys.argv[1]

    if fritz_action == '1':
        print(check_presence())
    elif fritz_action == '2':
        enable_wlan()
    elif fritz_action == '3':
        disable_wlan()


if __name__ == '__main__':
    execute()