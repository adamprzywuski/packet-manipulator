import asyncio
import queue
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from scapy.all import *
import logging

from show_interfaces import get_interfaces

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


class FilterParameters:
    interface = ""
    stop_index = 10
    packet_index = 0


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (InterfacePage, PacketPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InterfacePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "PacketPage":
            # self.after(20000, self.nothing())
            self.after(0, frame.do_asyncio())
            # frame.update_packets()

    def get_frame(self, page_name):
        return self.frames[page_name]


class InterfacePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.interface_list = get_interfaces()

        self.interface_listbox = ttk.Treeview(self)
        self.interface_listbox["columns"] = ("ipv4", "ipv6", "mac", "desc")
        self.interface_listbox.heading("#0", text="Name", anchor=tk.W)
        self.interface_listbox.heading("ipv4", text="IPv4", anchor=tk.W)
        self.interface_listbox.heading("ipv6", text="IPv6", anchor=tk.W)
        self.interface_listbox.heading("mac", text="MAC", anchor=tk.W)
        self.interface_listbox.heading("desc", text="Description", anchor=tk.W)

        i = 1
        for interface in self.interface_list:
            self.interface_listbox.insert("", i, i, text=interface.name, values=(interface.ipv4,
                                                                                 interface.ipv6,
                                                                                 interface.mac,
                                                                                 interface.desc))
            i = i + 1

        self.interface_listbox.pack(side=tk.TOP, fill=tk.X)

        self.select_button = tk.Button(self, text="Select", command=lambda: self.select())
        self.select_button.pack(pady=5)

    def select(self):
        FilterParameters.interface = self.interface_list[int(self.interface_listbox.focus()) - 1].name
        print(f"select: {FilterParameters.interface}")
        self.controller.get_frame("PacketPage").update_interface()
        self.controller.show_frame("PacketPage")


class PacketPage(tk.Frame, threading.Thread):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.the_queue = queue.Queue()
        self.controller = controller
        self.label = tk.Label(self, text=f"")
        self.label.pack(side="top", fill="x", pady=10)
        self.packet_table = ttk.Treeview(self)
        self.packet_table["columns"] = ("source", "destination", "protocol", "length", "info")
        self.packet_table.heading("#0", text="Time", anchor=tk.W)
        self.packet_table.heading("source", text="Source", anchor=tk.W)
        self.packet_table.heading("destination", text="Destination", anchor=tk.W)
        self.packet_table.heading("protocol", text="Protocol", anchor=tk.W)
        self.packet_table.heading("length", text="Length", anchor=tk.W)
        self.packet_table.heading("info", text="Info", anchor=tk.W)
        self.packet_table.pack(side=tk.TOP, fill=tk.X)
        self.packets = ["123", "456", "789"]
        self.consumer = ConsumerThread(self.the_queue, self.packet_table)
        self.producer = ProducerThread(self.the_queue)
        button = tk.Button(self, text="Change interface", command=lambda: controller.show_frame("InterfacePage"))
        button.pack(pady=10)

    def update_interface(self):
        print(f"update_interface: {FilterParameters.interface}")
        self.label.config(text=f"interface: {FilterParameters.interface}")

    def do_asyncio(self):
        self.producer.start()
        self.consumer.start()


class ConsumerThread(threading.Thread):
    def __init__(self, the_queue, table):
        super().__init__()
        self.the_queue = the_queue
        self.table = table

    def run(self):
        while True:
            self.refresh_data()

    def refresh_data(self, ):
        while not self.the_queue.empty():
            data = self.the_queue.get()
            logging.debug('get ' + str(data) + ' ' + str(FilterParameters.packet_index))
            self.table.insert("", tk.END, FilterParameters.packet_index, text=data)
            self.table.update_idletasks()
            FilterParameters.packet_index += 1


class ProducerThread(threading.Thread):
    def __init__(self, the_queue):
        super().__init__()
        self.the_queue = the_queue

    def run(self):
        while True:
            self.sniff_packets()

    def sniff_packets(self):
        packet = sniff(iface=FilterParameters.interface, count=1)
        logging.debug('create ' + packet[0].summary())
        self.the_queue.put(packet[0].summary())


if __name__ == "__main__":
    app = Gui()
    app.mainloop()
