import requests
import socket
import datetime


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

    def hora_atual(self):
            x = datetime.datetime.now()
            return x.strftime("%H:%M:%S")

