from scapy.all import *
import logging
import scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from model.ip_packet import IpPacket


def packet_callback(packet):
    if packet['TCP'].payload:
        pkt = str(packet['TCP'].payload)
        print(packet.proto)
        # if packet['IP'].dport == 80:
        print("\n{} ----HTTP----> {}:{}:\n{}".format(packet['IP'].src, packet['IP'].dst, packet['IP'].dport,
                                                     str(bytes(packet['TCP'].load))))

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
    #packets = sniff(count=5)
    #for p in packets:

     #   a = IpPacket(p)
      #  print(a)
    packet=Ether()/IP(dst='8.8.8.8')/TCP(dport=53,flags='S')
    send(packet)
