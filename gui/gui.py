import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont

from show_interfaces import get_interfaces


class FilterParameters:
    interface = ""


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
        self.myLabel = tk.Label(self, text="123")
        self.myLabel.pack(pady=5)

        self.select_button = tk.Button(self, text="Select", command=lambda: self.select())
        self.select_button.pack(pady=5)

    def select(self):
        FilterParameters.interface = self.interface_list[int(self.interface_listbox.focus())-1].name
        print(f"select: {FilterParameters.interface}")
        self.controller.get_frame("PacketPage").update_interface()
        self.controller.show_frame("PacketPage")


class PacketPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text=f"")
        self.label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Change interface", command=lambda: controller.show_frame("InterfacePage"))
        button.pack()

    def update_interface(self):
        print(f"update_interface: {FilterParameters.interface}")
        self.label.config(text=f"interface: {FilterParameters.interface}")


if __name__ == "__main__":
    app = Gui()
    app.mainloop()
