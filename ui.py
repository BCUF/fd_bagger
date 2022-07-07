###
# Copyright BCU Fribourg 2022
# Author: nstulz
###

from genericpath import exists
from json import load
import tkinter as tk
from tkinter import DISABLED, E, END, W, ttk
from tkinter.scrolledtext import ScrolledText
import re
from tkinter import filedialog
import os
import json
import logging
from logic import run
from constant import *
from tkinter import messagebox

logger = logging.getLogger(__name__)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)

        
        self.input_dir_value = tk.StringVar()
        self.output_dir_value = tk.StringVar()
        self.callnumber_value = tk.StringVar()
        self.fond_value = tk.StringVar()
        self.starting_number_value = tk.IntVar()
        self.metadata_value = tk.StringVar()
        self.mcp_value = tk.StringVar()
        self.process_value = tk.IntVar()

        self.run_btn = ttk.Button(self, text=BAG_BTN_TXT, state=DISABLED, command=self.start_running)

        self.log_text = ScrolledText(self, state='disabled')

        if os.path.exists(AUTO_SAVE_FILE):
            self.load_save()
            self.validate()

        self.build_gui()

    def start_running(self):

        self.save()

        # check if the lockfile is present or not
        mapping_file_name = f"{self.callnumber_value.get()}_mapping_lock.json"
        full_path = f"{os.getcwd()}{os.path.sep}{mapping_file_name}"
        if os.path.isfile(full_path):
            message = f"{full_path} all ready exists. You have to erase it manually if you want to restart completely, do you want to continue?"
            logger.info(message)
            answer = messagebox.askyesno(title='confirmation',
                        message=message)
            if not answer:
                logger.info("Stopped by user")
                return

        
        self.run_btn['state'] = tk.DISABLED

        run(self.input_dir_value.get(), 
            self.output_dir_value.get(), 
            self.callnumber_value.get(), 
            self.fond_value.get(), 
            self.starting_number_value.get(), 
            self.metadata_value.get(), 
            self.mcp_value.get(), 
            self.process_value.get())
        
        self.run_btn['state'] = tk.NORMAL

        messagebox.showinfo("Infos", "Finish")
        

    def load_save(self):
        with open(AUTO_SAVE_FILE, "r", encoding='utf-8') as json_file:
            data = json.loads(json_file.read())
            self.input_dir_value.set(data["input_dir"])
            self.output_dir_value.set(data["output_dir"])
            self.callnumber_value.set(data["callnumber"])
            self.fond_value.set(data["fond"])
            self.starting_number_value.set(data["starting_number"])
            self.metadata_value.set(data["metadata"])
            self.mcp_value.set(data["mcp"])
            self.process_value.set(data["process"])
            logger.info(f"{AUTO_SAVE_FILE } loaded")

    
    
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
        with open(AUTO_SAVE_FILE, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"saved in {AUTO_SAVE_FILE}")

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

    def build_gui(self):

        # input dir
        def open_in_dir():
            input_dir = filedialog.askdirectory()
            if input_dir:
                directory_path = os.path.abspath(input_dir)
                self.input_dir_value.set(directory_path)
                self.validate()
        input_dir_label = ttk.Label(self, text="Input directory * : ").grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=E)
        input_dir_btn = ttk.Button(self, text=BROWSE_BTN_TEXT, command=open_in_dir)
        input_dir_btn.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y, sticky=E)
        input_dir_value_label = ttk.Label(self, textvariable=self.input_dir_value).grid(column=1, row=0, padx=PAD_X, pady=PAD_Y)

        # output dir 
        def open_out_dir():
            output_dir = filedialog.askdirectory()
            if output_dir:
                directory_path = os.path.abspath(output_dir)
                self.output_dir_value.set(directory_path)
                self.validate()
        output_dir_label = ttk.Label(self, text="Output directory * : ").grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky=E)
        output_dir_btn = ttk.Button(self, text=BROWSE_BTN_TEXT, command=open_out_dir)
        output_dir_btn.grid(column=2, row=1, padx=PAD_X, pady=PAD_Y, sticky=E)
        output_dir_value_label = ttk.Label(self, textvariable=self.output_dir_value).grid(column=1, row=1, padx=PAD_X, pady=PAD_Y)


        # callnumber
        def cn_callback(var, index, mode):
            self.callnumber_value.set(self.callnumber_value.get())
            self.validate()            
        self.callnumber_value.trace_add('write', cn_callback)
        cn_label = ttk.Label(self, text="Callnumber * : ").grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky=E)
        cn_entry = ttk.Entry(self, width=ENTRY_WIDTH, textvariable=self.callnumber_value).grid(column=1, row=2, padx=PAD_X, pady=PAD_Y, sticky=E)
        
        # Fond
        def fd_callback(var, index, mode):
            self.fond_value.set(self.fond_value.get())
            self.validate()       
        self.fond_value.trace_add('write', fd_callback)
        fd_label = ttk.Label(self, text="Fond: ").grid(column=0, row=3, padx=PAD_X, pady=PAD_Y, sticky=E)
        fd_entry = ttk.Entry(self, width=ENTRY_WIDTH, textvariable=self.fond_value).grid(column=1, row=3, padx=PAD_X, pady=PAD_Y, sticky=E)

        # metadata
        def open_metadata_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                self.metadata_value.set(file_path)
                self.validate()       
        metadata_label = ttk.Label(self, text="Metadata file: ").grid(column=0, row=4, padx=PAD_X, pady=PAD_Y, sticky=E)
        metadata_btn = ttk.Button(self, text=BROWSE_BTN_TEXT, command=open_metadata_file).grid(column=2, row=4, padx=PAD_X, pady=PAD_Y, sticky=E)
        metadata_value_label = ttk.Label(self, textvariable=self.metadata_value).grid(column=1, row=4, padx=PAD_X, pady=PAD_Y)

        # mcp
        def open_MCP_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                self.mcp_value.set(file_path)
                self.validate()       
        mcp_label = ttk.Label(self, text="MCP file: ").grid(column=0, row=5, padx=PAD_X, pady=PAD_Y, sticky=E)
        mcp_btn = ttk.Button(self, text=BROWSE_BTN_TEXT, command=open_MCP_file).grid(column=2, row=5, padx=PAD_X, pady=PAD_Y, sticky=E)
        mcp_value_label = ttk.Label(self, textvariable=self.mcp_value).grid(column=1, row=5, padx=PAD_X, pady=PAD_Y)


        # start number
        def sn_callback(var, index, mode):
            self.starting_number_value.set(self.starting_number_value.get())
            self.validate()       
        self.starting_number_value.trace_add('write', sn_callback)
        sn_label = ttk.Label(self, text="Start Number: ").grid(column=0, row=6, padx=PAD_X, pady=PAD_Y, sticky=E)
        sn_entry = tk.Spinbox(self, from_=SN_MIN_VALUE, to=SN_MAX_VALUE, textvariable=self.starting_number_value).grid(column=1, row=6, padx=PAD_X, pady=PAD_Y, sticky=E)

        # number of process
        def np_callback(var, index, mode):
            self.process_value.set(self.process_value.get())
            self.validate()       
        self.process_value.trace_add('write', np_callback)
        np_label = ttk.Label(self, text="Process number: ").grid(column=0, row=7, padx=PAD_X, pady=PAD_Y, sticky=E)
        np_entry = ttk.Spinbox(self, from_=NP_MIN_VALUE, to=NP_MAX_VALUE, textvariable=self.process_value).grid(column=1, row=7, padx=PAD_X, pady=PAD_Y, sticky=E)

        # run button
        self.run_btn.grid(column=3, row=8, padx=PAD_X, pady=PAD_Y)
        
        self.log_text.grid(column=1, row=9, columnspan=3, padx=PAD_X, pady=PAD_Y)

        # Create textLogger
        text_handler = TextHandler(self.log_text)

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)



class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(END)
        self.text.after(0, append)