import tkinter as tk
from tkinter import font as tkfont
import logging

from gui.pages.interface_page import InterfacePage
from gui.pages.packet_page import PacketPage

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1100x400")
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
            self.after(0, frame.start_asyncio())

    def get_frame(self, page_name):

        return self.frames[page_name]


