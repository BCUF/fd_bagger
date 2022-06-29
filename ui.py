import tkinter as tk
from tkinter import E, W, ttk
import re
from tkinter import filedialog
import os

    # run(self.input_dir_value, self.output_dir_value, self.callnumber_value, self.fond_value, self.starting_number_value, self.metadata_value, self.mcp_value, self.process_value)

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

        # self.create_widgets()

        self.gui()


    def gui(self):

        # input dir
        def open_in_dir():
            input_dir = filedialog.askdirectory()
            if input_dir:
                directory_path = os.path.abspath(input_dir)
                ttk.Label(self, text=str(directory_path)).grid(column=2, row=0, padx=5, pady=5)
                self.input_dir_value = input_dir
        input_dir_label = ttk.Label(self, text="Input directory * : ").grid(column=0, row=0, padx=5, pady=5, sticky=E)
        input_dir_btn = ttk.Button(self, text="Browse", command=open_in_dir)
        input_dir_btn.grid(column=1, row=0, padx=5, pady=5, sticky=E)

        # output dir 
        def open_out_dir():
            output_dir = filedialog.askdirectory()
            if output_dir:
                directory_path = os.path.abspath(output_dir)
                ttk.Label(self, text=str(directory_path)).grid(column=2, row=1, padx=5, pady=5)
                self.output_dir_value = output_dir
        output_dir_label = ttk.Label(self, text="Output directory * : ").grid(column=0, row=1, padx=5, pady=5, sticky=E)
        output_dir_btn = ttk.Button(self, text="Browse", command=open_out_dir)
        output_dir_btn.grid(column=1, row=1, padx=5, pady=5, sticky=E)


        # callnumber
        def cn_callback(var):
            content = var.get()
            ttk.Label(self, text=content).grid(column=2, row=2, padx=5, pady=5)
        self.callnumber_value.trace("w", lambda name, index,mode, var=self.callnumber_value: cn_callback(self.callnumber_value))
        cn_label = ttk.Label(self, text="Callnumber * : ").grid(column=0, row=2, padx=5, pady=5, sticky=E)
        cn_entry = ttk.Entry(self, textvariable=self.callnumber_value)
        cn_entry.grid(column=1, row=2, padx=5, pady=5, sticky=E)
        
        # # Fond
        def fd_callback(var):
            content = var.get()
            ttk.Label(self, text=content).grid(column=2, row=3, padx=5, pady=5)
        self.fond_value.trace("w", lambda name, index,mode, var=self.fond_value: fd_callback(self.fond_value))
        fd_label = ttk.Label(self, text="Fond: ").grid(column=0, row=3, padx=5, pady=5, sticky=E)
        fd_entry = ttk.Entry(self, textvariable=self.fond_value).grid(column=1, row=3, padx=5, pady=5, sticky=E)

        # metadata
        def open_metadata_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                ttk.Label(self, text="The meta data file is : " + str(file_path)).grid(column=2, row=4, padx=5, pady=5)
                self.metadata_value = file
        metadata_label = ttk.Label(self, text="Metadata file: ").grid(column=0, row=4, padx=5, pady=5, sticky=E)
        metadata_btn = ttk.Button(self, text="Browse", command=open_metadata_file)
        metadata_btn.grid(column=1, row=4, padx=5, pady=5, sticky=E)

        # mcp
        def open_MCP_file():
            file = filedialog.askopenfilename()
            if file:
                file_path = os.path.abspath(file)
                ttk.Label(self, text="The MCP file is : " + str(file_path)).grid(column=2, row=5, padx=5, pady=5)
                self.mcp_value = file
        mcp_label = ttk.Label(self, text="MCP file: ").grid(column=0, row=5, padx=5, pady=5, sticky=E)
        mcp_btn = ttk.Button(self, text="Browse", command=open_MCP_file)
        mcp_btn.grid(column=1, row=5, padx=5, pady=5, sticky=E)


        # start number
        def sn_callback(var):
            content = var.get()
            ttk.Label(self, text=content).grid(column=2, row=6, padx=5, pady=5)
            self.starting_number_value.set(content)
        self.starting_number_value.trace("w", lambda name, index,mode, var=self.starting_number_value: sn_callback(self.starting_number_value))
        sn_label = ttk.Label(self, text="Start Number: ").grid(column=0, row=6, padx=5, pady=5, sticky=E)
        sn_entry = tk.Spinbox(self, from_=0, to=1000000, textvariable=self.starting_number_value)
        sn_entry.grid(column=1, row=6, padx=5, pady=5, sticky=E)

        # number of process
        def np_callback(var):
            content = var.get()
            ttk.Label(self, text=content).grid(column=2, row=7, padx=5, pady=5, sticky=W)
            self.process_value.set(content)
        self.process_value.set(4)
        self.process_value.trace("w", lambda name, index,mode, var=self.process_value: np_callback(self.process_value))
        np_label = ttk.Label(self, text="Process number: ").grid(column=0, row=7, padx=5, pady=5, sticky=E)
        np_entry = ttk.Spinbox(self, from_=1, to=16, textvariable=self.process_value)
        np_entry.grid(column=1, row=7, padx=5, pady=5, sticky=E)


        # run button
        run_btn = ttk.Button(self, text="BAG")
        run_btn.grid(column=3, row=8, padx=5, pady=5)

    # def callback(self, var):
    #     content = var.get()
    #     ttk.Label(self, text=content).grid(column=2, row=3, padx=5, pady=5, sticky=E)



    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # label
        ttk.Label(text='Email:').grid(row=0, column=0, padx=5, pady=5)

        # email entry
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid),)

        self.email_entry = ttk.Entry(self, width=50)
        self.email_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.email_entry.grid(row=0, column=1, columnspan=2, padx=5)

        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)

        # button
        self.send_button = ttk.Button(text='Send').grid(row=0, column=4, padx=5)

    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        self.email_entry['foreground'] = color

    def validate(self, value):
        """
        Validat the email entry
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            return False

        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.show_message('Please enter a valid email', 'red')


# if __name__ == '__main__':
#     app = App()
#     app.mainloop()