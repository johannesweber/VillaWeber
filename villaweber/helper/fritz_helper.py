from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.lib.fritzwlan import FritzGuestWLAN
from helper.configuration import Configuration


class FritzHelper:

    def __init__(self):
        self.configuration = None
        self.fh = None

        self.configuration = Configuration('villaweber')
        self.configuration.load()
        self.fh = FritzHosts(address=self.configuration.fritzbox_ip,
                             user=self.configuration.fritzbox_user,
                             password=self.configuration.fritzbox_pw)

    def is_present(self, residents):
        result = False
        hosts = self.fh.get_hosts_info()
        for index, host in enumerate(hosts, start=1):
            status = host['status']
            ip = host['ip']

            if ip in residents:
                result = status
                if status:
                    break

        return result

    def check_presence(self):
        residents = self.configuration.residents
        result = self.is_present(residents)
        return result

    def change_wlan_status(self, status, wlan_type, service=1):  # service 1 for 2.4 GHz, 2 for 5 GHz and 3 for a guest network.
        if wlan_type == 'guest':
            wlan = FritzGuestWLAN(address=self.configuration.fritzbox_ip,
                                  user=self.configuration.fritzbox_user,
                                  password=self.configuration.fritzbox_pw)
        else:
            wlan = FritzWLAN(address=self.configuration.fritzbox_ip,
                             user=self.configuration.fritzbox_user,
                             password=self.configuration.fritzbox_pw,
                             service=service)

        if status == 'off':
            wlan.disable()
        elif status == 'on':
            wlan.enable()
