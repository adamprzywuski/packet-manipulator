import queue
import threading
import tkinter as tk
import tkinter.ttk as ttk
from scapy.all import *
import re

from gui.threads.consumer_thread import ConsumerThread
from gui.parameters.filter_parameters import FilterParameters
from gui.parameters.global_parameters import GlobalParameters
from gui.threads.producer_thread import ProducerThread
from model.ip_packet import IpPacket


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
        packet=self.the_queue.get(item)
        print("you clicked on", packet)
        window=tk.Tk()
        window.title("Packet")
        window.geometry("400x400")
        label_source=tk.Label(window,text="Source",width=20)
        label_source.place(x=60,y=40)
        entry_source = tk.Entry(window)
        entry_source.place(x=160, y=40)
        entry_source.insert(0,packet.source)

        label_destination=tk.Label(window,text="Destination",width=20)
        label_destination.place(x=50,y=70)
        entry_destination = tk.Entry(window)
        entry_destination.place(x=160, y=70)
        entry_destination.insert(0,packet.destination)

        label_protocol=tk.Label(window,text="Protocol",width=20)
        label_protocol.place(x=60,y=100)
        entry_protocol = tk.Entry(window)
        entry_protocol.place(x=160, y=100)
        entry_protocol.insert(0,packet.protocol)

#TODO:Fixing placeholder for a RawData
        label_raw=tk.Label(window,text="Raw",width=20)
        label_raw.place(x=60,y=130)
        entry_raw = tk.Entry(window)
        entry_raw.place(x=160, y=130,height=100)
        entry_raw.insert(0,packet.info)



        button = tk.Button( window,text="Resend Packet", command=lambda:self.SendPacket(entry_destination.get(),entry_protocol.get(),packet.flags) )
        button.place(x=160,y=300)

    def SendPacket(self,destination,protocol,flag):


    #TODO:ADDING MAC ADRESSS WHICH WE SENDS DATA,because it using broadcast
        layer1=Ether()
        layer2=IP(dst=destination)
        if(protocol=="FTP"):
            layer3=TCP(dport=20, flags=flag)
        elif(protocol=="SSH"):
            layer3 =TCP(dport=22, flags=flag)
        elif (protocol == "Telnet"):
            layer3 =TCP(dport=23, flags=flag)
        elif (protocol == "SMTP"):
            layer3 =TCP(dport=25, flags=flag)
        elif (protocol == "DNS"):
            layer3 =TCP(dport=53, flags=flag)
        elif (protocol == "DHCP"):
            layer3 =UDP(dport=67, flags=flag)
        elif (protocol == "HTTP"):
            layer3 =TCP(dport=80, flags=flag)
        elif (protocol == "HTTPS"):
            layer3 =TCP(dport=443, flags=flag)
        else:
            regex=re.search('[0-9]+',protocol)
            port=int(regex.group(0))
            if(protocol[0]=='T'):
                #its TCP protocol
                layer3=TCP(dport=port,flags=flag)
            elif(protocol[0]=='U'):
                layer3=UDP(dport=port)

        try:
            sendp(layer1/layer2/layer3)
        except:
            print("Exception with sending packet")