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
        self.info = " "
        try:
            self.protocol = ip_proto(packet['IP']).upper()
        except:
            print("Exception with the protocols")
            self.protocol = packet['IP'].proto
            if(self.protocol==2):
                self.protocol="IGMP"
        if(self.protocol=='TCP' or self.protocol=='UDP'):
            self.info = str(bytes(packet[self.protocol].payload))
            if packet['IP'].dport==20 or packet['IP'].dport==21:
                self.protocol = "FTP"
            elif packet['IP'].dport==22:
                self.protocol = "SSH"
            elif packet['IP'].dport==23:
                self.protocol = "Telnet"
            elif packet['IP'].dport==25:
                self.protocol = "SMTP"
            elif packet['IP'].dport==53:
                self.protocol = "DNS"
            elif packet['IP'].dport==67 or packet['IP'].dport==68:
                self.protocol = "DHCP"
            elif packet['IP'].dport==80:
                self.protocol = "HTTP"
            elif packet['IP'].dport == 443:
                    self.protocol = "HTTPS"
            else:
                self.protocol=self.protocol+" : "+str(packet['IP'].dport)
        else:
            self.info=str(bytes(packet['Raw'].load))



    def __str__(self):
        return "Date: {0}, Source:{1}, Destination:{2}, Length:{3},Protocol:{4}, Info:{5}" \
            .format(self.time, self.source, self.destination, self.length, self.protocol, self.ttl)
