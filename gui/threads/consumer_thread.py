import logging
import threading
import tkinter as tk

from gui.parameters.global_parameters import GlobalParameters
from model.ip_packet import IpPacket

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


class ConsumerThread(threading.Thread):

    def __init__(self, packets_queue, table, packets_list):
        super().__init__()
        self.the_queue = packets_queue
        self.table = table
        self.packets_list: list = packets_list

    def run(self):
        while True:
            self.refresh_data()
            if self.the_queue.empty() and GlobalParameters.stop_thread_flag:
                break

    def refresh_data(self):
        while not self.the_queue.empty():
            data: IpPacket = self.the_queue.get()
            logging.debug('get ' + str(data) + ' ' + str(GlobalParameters.packet_index))
            self.packets_list.append(data)
            index = len(self.packets_list) - 1
            self.table.insert("", tk.END, index, text=index,
                              values=(data.source,
                                      data.destination,
                                      data.protocol,
                                      data.length,
                                      data.ttl))
            self.table.update_idletasks()
