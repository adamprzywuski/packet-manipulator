
import time
import scapy.all


def ip_proto(pkt):
    proto_field = pkt.get_field('proto')
    return proto_field.i2s[pkt.proto]

#TODO: ADDD A LOT OF IF TO SECURE THE CLASS

class Packet:

    date=""
    source=""
    destination=""
    protocol: str=""
    length=0
    info=""


    def __init__(self,packet):
        self.date=time.localtime()
        self.source=packet['IP'].src
        self.destination=packet['IP'].dst
        self.length=packet['IP'].len
        self.info=str(bytes(packet['Raw'].load))
        self.protocol=ip_proto(packet['IP'])



    def __str__(self):
        return "Date: {0}, Source:{1}, Destination:{2}, Length:{3},Protocol:{4}, Info:{5}".format(self.date,self.source,self.destination,self.length,self.protocol,self.info)

