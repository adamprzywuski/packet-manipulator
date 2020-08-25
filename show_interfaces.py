from scapy.arch import get_windows_if_list


class Interface(object):
    def __init__(self, name='', ipv4='', ipv6='', mac='', desc=''):
        self.name = name
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.mac = mac
        self.desc = desc


def get_interfaces():
    """returns a list of available network interfaces"""
    interfaces = []

    for iface in sorted(get_windows_if_list()):
        i = Interface(
            name=iface['name'],
            ipv4=iface['ips'][1],
            ipv6=iface['ips'][0],
            mac=iface['mac'],
            desc=iface['description']
        )
        interfaces.append(i)
    return interfaces


for iface in get_interfaces():
    print iface.name, iface.ipv4, iface.ipv6, iface.mac, iface.desc

print get_windows_if_list()
