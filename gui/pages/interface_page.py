import tkinter as tk
import tkinter.ttk as ttk
from gui.parameters.filter_parameters import FilterParameters
from model.interface import get_interfaces


class InterfacePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets()

    def select(self, event):
        FilterParameters.interface = self.interface_list[int(self.interface_listbox.focus())].name
        print(f"select: {FilterParameters.interface}")
        self.controller.get_frame("PacketPage").update_interface()
        self.controller.show_frame("PacketPage")

    def __create_widgets(self):
        label = tk.Label(self, text="Choose interface", font=self.controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.interface_list = get_interfaces()

        self.interface_listbox = ttk.Treeview(self)
        self.scrollbar = ttk.Scrollbar(self.interface_listbox, orient="vertical", command=self.interface_listbox.yview)
        self.interface_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.interface_listbox["columns"] = ("ipv4", "ipv6", "mac", "desc")
        self.interface_listbox.heading("#0", text="Name", anchor=tk.W)
        self.interface_listbox.heading("ipv4", text="IPv4", anchor=tk.W)
        self.interface_listbox.heading("ipv6", text="IPv6", anchor=tk.W)
        self.interface_listbox.heading("mac", text="MAC", anchor=tk.W)
        self.interface_listbox.heading("desc", text="Description", anchor=tk.W)

        i = 0
        for interface in self.interface_list:
            self.interface_listbox.insert("", tk.END, i, text=interface.name, values=(interface.ipv4,
                                                                                      interface.ipv6,
                                                                                      interface.mac,
                                                                                      interface.desc))
            i = i + 1

        self.interface_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.interface_listbox.bind("<Double-1>", lambda event: self.select(event=event))

        self.select_button = tk.Button(self, text="Select", command=lambda: self.select())
        self.select_button.pack(pady=5)
