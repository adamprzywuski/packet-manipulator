import logging
import threading

from scapy.sendrecv import sniff

from gui.parameters.filter_parameters import FilterParameters
from gui.parameters.global_parameters import GlobalParameters
from model.ip_packet import IpPacket

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


class ProducerThread(threading.Thread):
    def __init__(self, the_queue):
        super().__init__()
        self.the_queue = the_queue

    def run(self):
        while True:
            self.sniff_packets()
            if GlobalParameters.stop_thread_flag:
                break

    def sniff_packets(self):
        packet = sniff(iface=FilterParameters.interface, count=1)
        ip_packet = IpPacket(packet[0])
        logging.debug('create ' + packet[0].summary())
        self.the_queue.put(ip_packet)
