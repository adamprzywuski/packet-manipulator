import time
import scapy.all


def ip_proto(pkt):
    proto_field = pkt.get_field('proto')
    return proto_field.i2s[pkt.proto]


class IpPacket:
    def __init__(self, packet):
        self.time = time.clock()
        self.source = packet['IP'].src
        self.destination = packet['IP'].dst
        self.length = packet['IP'].len
        self.ttl = packet['IP'].ttl
        # self.info = str(bytes(packet['Raw'].load))
        self.protocol = ip_proto(packet['IP']).capitalize()

    def __str__(self):
        return "Date: {0}, Source:{1}, Destination:{2}, Length:{3},Protocol:{4}, Info:{5}" \
            .format(self.time, self.source, self.destination, self.length, self.protocol, self.ttl)
