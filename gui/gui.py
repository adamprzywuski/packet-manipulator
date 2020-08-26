import asyncio
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from scapy.all import *

from show_interfaces import get_interfaces


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
            self.after(2000, frame.update_packets())
            # frame.update_packets()

    def nothing(self):
        pass




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
        FilterParameters.interface = self.interface_list[int(self.interface_listbox.focus())-1].name
        print(f"select: {FilterParameters.interface}")
        self.controller.get_frame("PacketPage").update_interface()
        self.controller.show_frame("PacketPage")


class PacketPage(tk.Frame, threading.Thread):
    def __init__(self, parent, controller):
        self.asyncio_loop = asyncio.get_event_loop()
        tk.Frame.__init__(self, parent)
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
        button = tk.Button(self, text="Change interface", command=lambda: controller.show_frame("InterfacePage"))
        button.pack(pady=10)
        # self.update_packets()

    def run(self):
        self.asyncio_loop.run_until_complete(self.add_item())

    def update_interface(self):
        print(f"update_interface: {FilterParameters.interface}")
        self.label.config(text=f"interface: {FilterParameters.interface}")
        self.update_packets()

    async def add_item(self):
        tasks = [
            self.packets.append("666") for key in range(20)
            # self.update_packets()
        ]
        await asyncio.wait(tasks)

    async def do_data(self):
        """ Creating and starting 'maxData' asyncio-tasks. """
        tasks = [
            self.create_dummy_data(key) for key in range(self.max_data)
        ]
        await asyncio.wait(tasks)

    def update_packets(self):
        print("sniffing started")
        self.packet_table.pack(side=tk.TOP, fill=tk.X)
        # packets = sniff(iface=FilterParameters.interface, count=10)
        for item in self.packet_table.get_children():
            self.packet_table.delete(item)
        # self.packet_table.delete(*self.packet_table.get_children())
        for packet in self.packets:
            # self.packet_table.insert("", tk.END, FilterParameters.packet_index, text=packet.summary())
            self.packet_table.insert("", tk.END, FilterParameters.packet_index, text=packet)
            FilterParameters.packet_index += 1

        self.packet_table.update_idletasks()
        FilterParameters.stop_index -= 1
        print(f"sniffing step {FilterParameters.stop_index} finished")
        if FilterParameters.stop_index > -0:
            # time.sleep(2)
            # self.add_item()

        #     self.after(500, self.controller.show_frame("PacketPage"))
        # print("sniffing finished")



if __name__ == "__main__":
    app = Gui()
    app.mainloop()
