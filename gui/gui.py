import time
import tkinter as tk
from tkinter import font as tkfont

# global interface
# global INTERFACE
INTERFACE = "123"


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("400x400")

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

        interface_list = ["Ethernet 1", "Ethernet 2", "Ethernet 3"]

        self.interface_listbox = tk.Listbox(self)
        for interface in interface_list:
            self.interface_listbox.insert(tk.END, interface)
        self.interface_listbox.pack(pady=15)

        self.myLabel = tk.Label(self, text="123")
        self.myLabel.pack(pady=5)

        self.select_button = tk.Button(self, text="Select", command=lambda: self.select())
        self.select_button.pack(pady=5)

    def select(self):
        # self.myLabel.config(text=self.interface_listbox.get(tk.ANCHOR))
        global INTERFACE
        INTERFACE = self.interface_listbox.get(tk.ANCHOR)
        print(f"select: {INTERFACE}")
        # print(self.controller.interface)
        # print(INTERFACE)
        self.controller.get_frame("PacketPage").update_interface(INTERFACE)
        self.controller.show_frame("PacketPage")


class PacketPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.interface = "aaa"
        print(f"packet: {INTERFACE}")
        self.label = tk.Label(self, text=f"You successfully chosen {INTERFACE}")
        self.label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Change interface", command=lambda: controller.show_frame("InterfacePage"))
        button.pack()

    def update_interface(self, interface):
        self.interface = interface
        print(f"update_interface: {self.interface}")
        self.label.config(text=f"interface: {self.interface}")



if __name__ == "__main__":
    app = Gui()
    app.mainloop()
