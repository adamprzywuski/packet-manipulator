import queue
import threading
import tkinter as tk
import tkinter.ttk as ttk

from gui.threads.consumer_thread import ConsumerThread
from gui.parameters.filter_parameters import FilterParameters
from gui.parameters.global_parameters import GlobalParameters
from gui.threads.producer_thread import ProducerThread


class PacketPage(tk.Frame, threading.Thread):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.the_queue = queue.Queue()
        self.controller = controller
        self.__create_widgets()

        self.consumer = any
        self.producer = any

    def update_interface(self):
        print(f"update_interface: {FilterParameters.interface}")
        self.label.config(text=f"interface: {FilterParameters.interface}")

    def start_asyncio(self):
        self.packet_table.delete(*self.packet_table.get_children())
        GlobalParameters.packet_index = 0
        self.do_asyncio()

    def do_asyncio(self):
        GlobalParameters.stop_thread_flag = False
        self.consumer = ConsumerThread(self.the_queue, self.packet_table)
        self.producer = ProducerThread(self.the_queue)
        self.producer.start()
        self.consumer.start()

    def join_threads(self):
        GlobalParameters.stop_thread_flag = True
        self.producer.join()
        self.consumer.join()

    def change_interface(self):
        self.join_threads()
        self.controller.show_frame("InterfacePage")



    def __create_widgets(self):
        self.label = tk.Label(self, text=f"")
        self.label.pack(side="top", fill="x", pady=10)

        self.packet_table = ttk.Treeview(self)
        self.scrollbar = ttk.Scrollbar(self.packet_table, orient="vertical", command=self.packet_table.yview)
        self.packet_table.configure(yscrollcommand=self.scrollbar.set)
        self.packet_table["columns"] = ("source", "destination", "protocol", "length", "ttl")
        self.packet_table.heading("#0", text="Time", anchor=tk.W)
        self.packet_table.heading("source", text="Source", anchor=tk.W)
        self.packet_table.heading("destination", text="Destination", anchor=tk.W)
        self.packet_table.heading("protocol", text="Protocol", anchor=tk.W)
        self.packet_table.heading("length", text="Length", anchor=tk.W)
        self.packet_table.heading("ttl", text="TTL", anchor=tk.W)
        self.packet_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.packet_table.bind("<Double-1>", self.OnDoubleClick)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        button_side = tk.RIGHT
        button = tk.Button(button_frame, text="Change interface", command=lambda: self.change_interface())
        button.pack(side=tk.LEFT, padx=10)
        button = tk.Button(button_frame, text="Start", command=lambda: self.do_asyncio())
        button.pack(side=button_side, padx=10)
        button = tk.Button(button_frame, text="Stop", command=lambda: self.join_threads())
        button.pack(side=button_side)

    def OnDoubleClick(self, event):
        item = self.packet_table.selection()[0]
        print("you clicked on", self.the_queue.get(item))
        window=tk.Tk()
        window.title("Packet")
        window.geometry("400x200")
        #txt=tk.Entry(window,width=10)
        #txt.grid(column=1,row=0)
