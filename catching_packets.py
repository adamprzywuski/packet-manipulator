from scapy.all import *
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def packet_callback(packet):
    if packet['TCP'].payload:
        pkt = str(packet['TCP'].payload)

        # if packet['IP'].dport == 80:
        print("\n{} ----HTTP----> {}:{}:\n{}".format(packet['IP'].src, packet['IP'].dst, packet['IP'].dport,
                                                     str(bytes(packet['TCP'].payload))))

        # print(get_host_for_ip(packet['IP'].src))
        sniff(filter="tcp", prn=packet_callback, store=0)


# allows to exchange ip to http adress
def get_host_for_ip(ip):
    try:
        host = socket.gethostbyaddr(ip)
    except socket.error:
        return ip
    return host


if __name__ == '__main__':
    print("program wlaczony")
    packets = sniff(iface="WiFi", count=10)
    print(packets[0])
    summary = packets[0].summary()
    print(summary)
