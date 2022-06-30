from genericpath import exists
from json import load
import tkinter as tk
from tkinter import DISABLED, E, W, ttk
import re
from tkinter import filedialog
import os
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('BCUF FD_BAGGER')
        self.geometry("700x350")

        
        self.input_dir_value = tk.StringVar()
        self.output_dir_value = tk.StringVar()
        self.callnumber_value = tk.StringVar()
        self.fond_value = tk.StringVar()
        self.starting_number_value = tk.IntVar()
        self.metadata_value = tk.StringVar()
        self.mcp_value = tk.StringVar()
        self.process_value = tk.IntVar()

        self.run_btn = ttk.Button(self, text="BAG", state=DISABLED, command=self.start_running)

        if os.path.exists("save.json"):
            self.load_save()
            self.validate()

        self.gui()

    def start_running(self):
        print("start_running")
        # run(self.input_dir_value, self.output_dir_value, self.callnumber_value, self.fond_value, self.starting_number_value, self.metadata_value, self.mcp_value, self.process_value)


    def load_save(self):
        with open("save.json", "r", encoding='utf-8') as json_file:
            data = json.loads(json_file.read())
            self.input_dir_value.set(data["input_dir"])
            self.output_dir_value.set(data["output_dir"])
            self.callnumber_value.set(data["callnumber"])
            self.fond_value.set(data["fond"])
            self.starting_number_value.set(data["starting_number"])
            self.metadata_value.set(data["metadata"])
            self.mcp_value.set(data["mcp"])
            self.process_value.set(data["process"])
    
    
    def save(self):
        data = {}
        data["input_dir"] = self.input_dir_value.get()
        data["output_dir"] = self.output_dir_value.get()
        data["callnumber"] = self.callnumber_value.get()
        data["fond"] = self.fond_value.get()
        data["starting_number"] = self.starting_number_value.get()
        data["metadata"] = self.metadata_value.get()
        data["mcp"] = self.mcp_value.get()
        data["process"] = self.process_value.get()
        with open("save.json", "w", encoding='utf-8') as json_file:
            json.dump(data, json_file)

    def print_state(self):
        print(f"input dir: {self.input_dir_value.get()}")
        print(f"output dir: {self.output_dir_value.get()}")
        print(f"callnumber: {self.callnumber_value.get()}")
        print(f"fond: {self.fond_value.get()}")
        print(f"starting_number: {self.starting_number_value.get()}")
        print(f"metadata: {self.metadata_value.get()}")
        print(f"mcp: {self.mcp_value.get()}")
        print(f"process: {self.process_value.get()}")


    def validate(self):
        is_valid = False
        self.print_state()
        if os.path.isdir(self.input_dir_value.get()):
            is_valid = True
        else:
            is_valid = False
        if os.path.isdir(self.output_dir_value.get()):
            is_valid = True
        else:
            is_valid = False     
        if len(self.callnumber_value.get()) > 0:
            is_valid = True
        else:
            is_valid = False
        if is_valid:
            self.run_btn['state'] = tk.NORMAL
        else:
            self.run_btn['state'] = tk.DISABLED

    def gui(self):

        # input dir
        def open_in_dir():
            input_dir = filedialog.askdirectory()
            if input_dir:
                directory_path = os.path.abspath(input_dir)
                self.input_dir_value.set(directory_path)
                self.validate()
        input_dir_label = ttk.Label(self, text="Input directory * : ").grid(column=0, row=0, padx=5, pady=5, sticky=E)
        input_dir_btn = ttk.Button(self, text="Browse", command=open_in_dir)
        input_dir_btn.grid(column=2, row=0, padx=5, pady=5, sticky=E)
        input_dir_value_label = ttk.Label(self, textvariable=self.input_dir_value).grid(column=1, row=0, padx=5, pady=5)

        # output dir 
        def open_out_dir():
            output_dir = filedialog.askdirectory()
            if output_dir:
                directory_path = os.path.abspath(output_dir)
                self.output_dir_value.set(directory_path)
                self.validate()
        output_dir_label = ttk.Label(self, text="Output directory * : ").grid(column=0, row=1, padx=5, pady=5, sticky=E)
        output_dir_btn = ttk.Button(self, text="Browse", command=open_out_dir)
        output_dir_btn.grid(column=2, row=1, padx=5, pady=5, sticky=E)
        output_dir_value_label = ttk.Label(self, textvariable=self.output_dir_value).grid(column=1, row=1, padx=5, pady=5)


        # callnumber
        def cn_callback(var, index, mode):
            self.callnumber_value.set(self.callnumber_value.get())
            self.validate()            
        self.callnumber_value.trace_add('write', cn_callback)
        cn_label = ttk.Label(self, text="Callnumber * : ").grid(column=0, row=2, padx=5, pady=5, sticky=E)
        cn_entry = ttk.Entry(self, textvariable=self.callnumber_value).grid(column=1, row=2, padx=5, pady=5, sticky=E)
        
        # Fond
        def fd_callback(var, index, mode):
            self.fond_value.set(self.fond_value.get())
            self.validate()       
        self.fond_value.trace_add('write', fd_callback)
        fd_label = ttk.Label(self, text="Fond: ").grid(column=0, row=3, padx=5, pady=5, sticky=E)
        fd_entry = ttk.Entry(self, textvariable=self.fond_value).grid(column=1, row=3, padx=5, pady=5, sticky=E)

        # metadata
        def open_metadata_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                self.metadata_value.set(file_path)
                self.validate()       
        metadata_label = ttk.Label(self, text="Metadata file: ").grid(column=0, row=4, padx=5, pady=5, sticky=E)
        metadata_btn = ttk.Button(self, text="Browse", command=open_metadata_file)
        metadata_btn.grid(column=2, row=4, padx=5, pady=5, sticky=E)
        metadata_value_label = ttk.Label(self, textvariable=self.metadata_value).grid(column=1, row=4, padx=5, pady=5)

        # mcp
        def open_MCP_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                self.mcp_value.set(file_path)
                self.validate()       
        mcp_label = ttk.Label(self, text="MCP file: ").grid(column=0, row=5, padx=5, pady=5, sticky=E)
        mcp_btn = ttk.Button(self, text="Browse", command=open_MCP_file)
        mcp_btn.grid(column=2, row=5, padx=5, pady=5, sticky=E)
        mcp_value_label = ttk.Label(self, textvariable=self.mcp_value).grid(column=1, row=5, padx=5, pady=5)


        # start number
        def sn_callback(var, index, mode):
            self.starting_number_value.set(self.starting_number_value.get())
            self.validate()       
        self.starting_number_value.trace_add('write', sn_callback)
        sn_label = ttk.Label(self, text="Start Number: ").grid(column=0, row=6, padx=5, pady=5, sticky=E)
        sn_entry = tk.Spinbox(self, from_=0, to=1000000, textvariable=self.starting_number_value).grid(column=1, row=6, padx=5, pady=5, sticky=E)

        # number of process
        def np_callback(var, index, mode):
            self.process_value.set(self.process_value.get())
            self.validate()       
        self.process_value.trace_add('write', np_callback)
        np_label = ttk.Label(self, text="Process number: ").grid(column=0, row=7, padx=5, pady=5, sticky=E)
        np_entry = ttk.Spinbox(self, from_=1, to=16, textvariable=self.process_value).grid(column=1, row=7, padx=5, pady=5, sticky=E)


        # run button
        self.run_btn.grid(column=3, row=8, padx=5, pady=5)