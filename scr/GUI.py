import tkinter as tk
from tkinter import NSEW, NW, Frame, StringVar, Variable, ttk
import requests
import socket


class MainICMP(tk.Frame):
    def __init__(self, container):
        super().__init__(container, bg="#ffffff")
        
        ############ CRIANDO LABEL FRAME PING ########## 
        self.frame1 = Frame(self)
        self.labelframe1 = ttk.LabelFrame(self, text='PING')
        self.frame2 = Frame(self)

        ############ VARIAVEIS DOS MODULOS ########## 

        self.ip = MyIP()
        self.row = {"row":0}
        self.ping_var = {
            "HOST": [],
            "QTD": [],
            "SIZE": []
        }

        
        self.__label_ip_time()
        self.__create_widgets()
        self.__label_entry_ping()
        self.__button_label()

    def __label_ip_time(self):

        ############ CRIANDO LABEL SUPERIOR ############ 
        label1 = tk.Label(self.frame1, text=f"IP local: {self.ip.IP_Host()}", width=20, height=2, font=('Arial 10 bold'))
        label1.grid(row=0, column=0, padx=5, pady=10)

        label2 = tk.Label(self.frame1, text=f"IP Public: {self.ip.IP_Public()}", width=20, height=2, font=('Arial 10 bold'))
        label2.grid(row=0, column=1, padx=5, pady=10)

        label3 = tk.Label(self.frame1, text="Hora: 12:42:52", width=15, height=2, font=('Arial 10 bold'))
        label3.grid(row=0, column=2, padx=5, pady=10)


    def __label_entry_ping(self):
        ######### LABEL PING ###########
        r = self.row["row"]
        self.host_var = StringVar()
        self.size_var = StringVar()
        self.qtd_var = StringVar()
        
        
        label_host = tk.Label(self.labelframe1, text="HOST:")
        label_host.grid(row=r, column=0, pady=5)

        label_host = tk.Label(self.labelframe1, text="SIZE:")
        label_host.grid(row=r, column=2, pady=5)

        label_host = tk.Label(self.labelframe1, text="QTD:")
        label_host.grid(row=r, column=4, pady=5)

        ######### RECEBE VALORES PARA PING ###########

        entry_host = ttk.Entry(self.labelframe1, textvariable=self.host_var)
        entry_host.grid(row=r, column=1, pady=5)

        entry_size = ttk.Entry(self.labelframe1, textvariable=self.size_var)
        entry_size.grid(row=r, column=3, pady=5)

        entry_qtd = ttk.Entry(self.labelframe1, textvariable=self.qtd_var)
        entry_qtd.grid(row=r, column=5, pady=5)
        
        if r <= 10:
            self.row["row"] += 1
            pass
        print(self.row)

    
    def __button_label(self):
        ######### BUTTON PARA ADICIONAR NOVO PING ###########
        r = self.row["row"]
        self.button1 = ttk.Button(self.labelframe1, text="+", width=10, command=self.__label_entry_ping)
        self.button1.grid(row=0, column=6)

        self.button2 = ttk.Button(self.frame2, text="Start", width=10, command=self.__test)
        self.button2.grid(row=0, column=0)


    def __test(self):
     
        print(self.host_var.get(), "\n")
        print(self.size_var.get(), "\n")
        print(self.qtd_var.get(), "\n")


    def __create_widgets(self):
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        self.frame2.grid(row=3, column=0, padx=10, pady=10, sticky=NSEW)


        self.labelframe1.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky=NW)

        self.grid(row=0, column=0)


class MyIP():
    # Retorna o IP publico. 
    def IP_Public(self):
        return requests.get('http://meuip.com/api/meuip.php').text
         


    # Retorna o IP gateway
    def IP_Gateway(self):
        pass


    # Retorna o IP do host
    def IP_Host(self):
        return socket.gethostbyname(socket.gethostname())


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ICMP')
        self.geometry('630x500+700+200')
        self.configure(background='#ffffff')
        
        self.__create_widgets()


    def __create_widgets(self):
        MainICMP(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()