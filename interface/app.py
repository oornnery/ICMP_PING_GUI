import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from tkinter.messagebox import showerror, showinfo

from matplotlib.figure import Figure
from scr.modules import date_now, dns_resolver, tracert, ping, write_log, read_file, Calculate
from interface.variables import portais
import threading
import matplotlib.pyplot as plt
import numpy as np

class TabPing(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        """
        Label MTR
        """
        # Name of the frame
        self.configure(text='Address PING')
        # Size of the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        # Variables 

        self.select = None # variable to select the host
        self.path = ".\\log\\" # path to the log
        self.hosts = {
        
        } # variable to save the hosts
        self.cont = 0 # variable to count the text

        self.entry_var = StringVar() # variable to save the input hosts
        self.cbo_1_var = StringVar() # variable to save the combobox

        self.column_name = {
            'host': ('Host', 100), 
            'stt': ('Stt', 60), 
            'times': ('Times', 60),
            'pct_sent': ("Sent", 60),
            'pct_recv': ("Recv", 60),
            'pct_loss': ("Loss", 60),
            'rtt_best': ("Rtt Best", 60),
            'rtt_avg': ("Rtt Avg", 60),
            'rtt_worst': ("Rtt Worst", 60),
            'jtt_best': ("Jtt Best", 60),
            'jtt_avg': ("Jtt Avg", 60),
            'jtt_worst': ("Jtt Worst", 60),
            'ttl': ('TTL', 60), 
            'Last': ('Last', 60)} # Table tree Ping



        # Widgets
        # Label select portal
        self.lbl_1 = ttk.Label(self, text='Select Portal: ') 
        self.lbl_1.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        

        # Combobox select portal
        self.cbo_1 = ttk.Combobox(self, textvariable=self.cbo_1_var)
        self.cbo_1.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.cbo_1['values'] = list(portais.keys()) # list of portals
        self.cbo_1.current(0) # set the first item as default
        self.cbo_1.bind('<<ComboboxSelected>>', self.select_cbo_1) # bind the event


        # Label entry
        self.lbl_2 = ttk.Label(self, text='Host ex. 192.168.1.1: ')
        self.lbl_2.grid(row=1, column=0, sticky='w', padx=5, pady=5)


        # Entry input hosts
        self.entry_1 = ttk.Entry(self, textvariable=self.entry_var)
        self.entry_1.grid(row=1, column=1, sticky='w', padx=5, pady=5)


        # Button add hosts
        self.btn_1 = ttk.Button(self, text='Add', command=lambda: self.validate_ip())
        self.btn_1.grid(row=1, column=2, sticky='w', padx=5, pady=5)

        # Table Treeview
        self.tree = ttk.Treeview(self, columns=list(self.column_name.keys()), show='headings')
        for tree, text in self.column_name.items():
            self.tree.heading(tree, text=text[0])
            self.tree.column(tree, minwidth=0, width=text[1])

        self.tree.bind('<<TreeviewSelect>>', self.tree_selected)
        self.tree.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        

        # Button run
        self.btn_2 = ttk.Button(self, text='Run', command=lambda: self.run_ping(self.select))
        self.btn_2.grid(row=3, column=1, sticky='e', padx=5, pady=5)


        # Button stop
        self.btn_3 = ttk.Button(self, text='Stop', command=lambda: self.stop_ping(self.select))
        self.btn_3.grid(row=3, column=2, sticky='e', padx=5, pady=5)

        # Button plot
        self.btn_4 = ttk.Button(self, text='Plot', command=lambda: print('Table'))
        self.btn_4.grid(row=3, column=3, sticky='e', padx=5, pady=5)

        # Text output
        self.text = tk.Text(self, height=5)
        self.add_text('Ping is running...') # insert text


        # Button Show Output
        self.btn_5 = ttk.Button(self, text='Command', command=lambda: self.show_output())
        self.btn_5.grid(row=5, column=0, sticky='w', padx=5, pady=5)


        # Button Exit
        self.btn_6 = ttk.Button(self, text='Exit', command=lambda: self.destroy())
        self.btn_6.grid(row=5, column=3, sticky='e', padx=5, pady=5)


        self.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        threading.Thread(target=self.pping).start()


    def select_cbo_1(self, event):
        """
        Event when the combobox is selected
        """
        self.cbo_1.configure(state='disabled') # disable the combobox
        self.add_text(f'{self.cbo_1_var.get()} is selected!') # insert text
        self.add_host(portais[self.cbo_1_var.get()]) # insert hosts 
        self.tree_update() # update the treeview


    
    def validate_ip(self):
        """
        Validate the input hosts
        """
        hosts = self.entry_var.get().replace(' ', '').split(',') # get the input hosts

        if hosts != ['']: # if the input hosts is not empty
            for ip in hosts:
                if dns_resolver(ip)[0] == 0: # if the ip is valid
                    self.add_host(ip) # insert host
                    self.add_text(f'{ip} is added!') # insert text
                    self.tree_update() # update the treeview

                else:  # if not valid:
                    showerror(title='Information',
                            message=f'Hello, {ip} is not a valid IPv4 address!') # show error
                    self.add_text(f'{ip} is not a valid IPv4 address!') # insert text

            self.entry_var.set('') # clear the input


    def tree_selected(self, event):
        """
        Event when the item is selected
        """
        for selected_item in self.tree.selection():
            result = self.tree.item(selected_item, 'values')[0]
            self.select = result
            self.add_text(f'{result} is selected!') # insert text


    def add_host(self, host):
        """
        Add a host to the dictionary
        """
        self.hosts.update({host: {'host': host, 'status': 'OFF', 'times': [],
                                'pct_sent': 0, 'pct_recv': 0, 'pct_loss': 0, 
                                'rtt_best': 0, 'rtt_avg': 0, 'rtt_worst': 0, 
                                'jtt_best': 0, 'jtt_avg': 0, 'jtt_worst': 0,
                                'ttl': 0, 'Last': 0}}) # add host to the dictionary

        self.add_text(f'{host} is added!') # insert text


    def run_ping(self, host):
        """
        Run the ping command
        """
        try:
            self.hosts[host]['status'] = 'ON' # set the status to ON
            self.add_text(f' Run {host}')
            self.tree_update() # update the treeview
        except KeyError:
            self.add_text(f'{host} is not added!')


    def stop_ping(self, host):
        """
        Stop the ping command
        """
        try:
            self.hosts[host]['status'] = 'OFF' # set the status to OFF
            self.add_text(f' Stop {host}')
            self.tree_update() # update the treeview
        except KeyError:
            self.add_text(f'{host} is not added!')


    def add_text(self, text):
        """
        Add text to the text output
        """
        self.text.insert(tk.END, f"\n [{self.cont}] {date_now()} :: {text}")
        self.cont += 1


    def show_output(self):
        """
        Show the output of the command
        """
        if self.text.grid_info() != {}:
            self.text.grid_forget()
        else:
            self.text.grid(row=4, column=0, columnspan=4, sticky='we', padx=5, pady=5) # show the text


    def pping(self):
        """
        Run the ping command
        """
        try:
            for key in self.hosts.keys():
                host = self.hosts[key]['host']

                if self.hosts[key]['status'] == 'ON':
                    self.add_text(f' Run {host}')
                    
                    # Run the ping command
                    write_log(key, ping(host))


                    # Update the treeview
                    self.dict_update(read_file(key), key)

                    self.tree_update()


                else:
                    self.add_text(f'{self.hosts[key]["host"]} is stopped')
                    continue
                    
        except Exception as e:
            print(e)
        
        self.after(1000, self.pping)


    def tree_update(self):
        """
        Update value of the tree
        """
        try:
            self.tree.delete(*self.tree.get_children())
            
            for host in self.hosts.values():
                self.tree.insert('', tk.END, values=list(host.values()))

        except IndexError:
            pass


    def dict_update(self, rtts: list, key: str):
        """
        """
        cal = Calculate(rtts[2])
        # Update Loss
        loss = cal.calc_loss()
        self.hosts[key]["pct_sent"] = loss[0]
        self.hosts[key]["pct_recv"] = loss[1]
        self.hosts[key]["pct_loss"] = loss[2]


        # Update Rtt
        rtt = cal.calc_rtts()
        self.hosts[key]["rtt_best"] = rtt[0]
        self.hosts[key]["rtt_avg"] = rtt[1]
        self.hosts[key]["rtt_worst"] = rtt[2]
        


        # Update Jitter
        jitter = cal.calc_jitter()
        self.hosts[key]["jtt_best"] = jitter[1]
        self.hosts[key]["jtt_avg"] = jitter[2]
        self.hosts[key]["jtt_worst"] = jitter[3]

        self.hosts[key]["ttl"] = rtts[3]
        self.hosts[key]["times"] = rtts[0][-1]



def plot(self, key):
    """
    Plot the data
    """
   
    # Create a new figure
    fig = plt.figure(figsize=(10, 5))

    # Create a new subplot
    value = read_file(key)
    calc = Calculate.calc_jitter(value[2])

    rtt = [value[0], value[2], calc[0]]

    # Create a new subplot
    # create a figure
    figure = Figure(figsize=(6, 4), dpi=100)

    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, self)

    # create the toolbar
    NavigationToolbar2Tk(figure_canvas, self)

    # create axes
    axes = figure.add_subplot()

    # create the barchart
    axes.bar(languages, popularity)
    axes.set_title('Top 5 Programming Languages')
    axes.set_ylabel('Popularity')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

   

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N2P Monitor - 1.0")
        #self.geometry("800x600")
        #self.resizable(False, False)
        self.configure(background='#f0f0f0')
        self.configure(relief='flat')

        # Grids
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Menu de opções
        value_menu = {
            'File': {'Open': self.pp('Open'), 'Save': self.pp('Save'), '-': None ,'Exit': self.quit},
            'Edit': {'Copy': self.pp('Copy'), 'Paste': self.pp('Paste'), 'Undo': self.pp('Undo')},
            'Help': {'About': self.pp('Abot'), 'Update': self.pp('Update')}
        }
        self.create_menu(value_menu)

    
        # Frame IP
        self.frame_label_ip = ttk.Label(self)
        self.frame_label_ip.configure(background='#363636')
        self.frame_label_ip.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

        self.create_label_ip(self.frame_label_ip)

        # Frame bar button
        self.frame_bar_button = ttk.Label(self)
        self.frame_bar_button.configure(background='#f0f0f0')
        self.frame_bar_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        value_button = {
            'PING': (lambda: self.notebook.add(TabPing(self.notebook), text='Ping'), 'button.png' ),
            'MTR': (lambda: self.notebook.add(TabPing(self.notebook), text='MTR'), 'button.png' ),
            'SIP ALG': (self.pp('Sip Alg'), 'button.png' ),
            'NMAP': (self.pp('Nmap'), 'button.png' ),
        }
        self.create_bar_button(self.frame_bar_button, value_button)

        # Frame notebook
        self.frame_notebook = ttk.Label(self)
        self.frame_notebook.configure(background='#f0f0f0')
        self.frame_notebook.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Notebook 
        self.notebook = ttk.Notebook(self.frame_notebook)
        self.notebook.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        

    def run(self):
        self.mainloop()
    

    def create_menu(self, parameter=None):
        menu = tk.Menu(self)
        self.config(menu=menu)

        for key, value in parameter.items():
            menu_item = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label=key, menu=menu_item)
            for label, command in value.items():
                if label == '-':
                    menu_item.add_separator()
                else: 
                    menu_item.add_command(label=label, command=command)
    

    def create_label_ip(self, frame=None):

        # Label         
        self.label_1 = ttk.Label(frame)
        self.label_1.configure(text='IP local:', font=('Arial', 10, 'italic bold'), 
                            foreground='#ffffff', background='#363636')

        self.label_1.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

        self.label_2 = ttk.Label(frame)
        self.label_2.configure(text='255.255.255.1', font=('Arial', 10, 'italic normal'), 
                            foreground='#ffffff', background='#363636')

        self.label_2.grid(row=0, column=1, sticky='n', padx=5, pady=5)

        self.label_3 = ttk.Label(frame)
        self.label_3.configure(text='IP Publico', font=('Arial', 10, 'italic bold'), 
                            foreground='#ffffff', background='#363636')

        self.label_3.grid(row=0, column=2, sticky='ne', padx=5, pady=5)
        
        self.label_4 = ttk.Label(frame)
        self.label_4.configure(text='255.255.255.1', font=('Arial', 10, 'italic normal'), 
                            foreground='#ffffff', background='#363636')

        self.label_4.grid(row=0, column=3, sticky='ne', padx=5, pady=5)


    def create_bar_button(self, frame, parameter=None):
        row = 0
        for key, value in parameter.items():
            icon = tk.PhotoImage(file=r'.\images\button.png')
            iconn = icon.subsample(3, 3)
            button = ttk.Button(frame)
            button.configure(image=iconn, text=key, compound='left', command=value[0])
            button.grid(row=row, column=0, sticky='nw', padx=5, pady=5)
            row += 1
        

    def function_button_1(self):
        ...
    
    def pp(self, text):
        return lambda: print(text)

        