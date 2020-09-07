import logging
import threading
import tkinter as tk

from gui.parameters.global_parameters import GlobalParameters
from model.ip_packet import IpPacket

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


class ConsumerThread(threading.Thread):

    def __init__(self, the_queue, table):
        super().__init__()
        self.the_queue = the_queue
        self.table = table

    def run(self):
        while True:
            self.refresh_data()
            if self.the_queue.empty() and GlobalParameters.stop_thread_flag:
                break

    def refresh_data(self, ):
        while not self.the_queue.empty():
            data: IpPacket = self.the_queue.get()
            logging.debug('get ' + str(data) + ' ' + str(GlobalParameters.packet_index))
            self.table.insert("", tk.END, GlobalParameters.packet_index, text=GlobalParameters.packet_index,
                              values=(data.source,
                                      data.destination,
                                      data.protocol,
                                      data.length,
                                      data.ttl))
            self.table.update_idletasks()
            GlobalParameters.packet_index += 1


