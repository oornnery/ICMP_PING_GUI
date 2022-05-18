from datetime import datetime
import os
import platform
import re
import socket
import subprocess
from time import time

import requests

def date_now():
    return datetime.strftime(datetime.now(), '%H:%M:%S')




def validate_ipv4(address):
    try:
        socket.inet_aton(address)
        return (0, address)
    
    except socket.error as e:
        return (1, address)




def dns_resolver(host):
    """
    Resolver o DNS
    host: Host a ser resolvido
    Return: Ipv4
    """
    try:
        socket.gethostbyname(host)
        return (0, socket.gethostbyname(host))
    
    except socket.gaierror as e:
        print(e)
        return (1, host)




def tracert(address):
    ipv4 = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    try:
        # Run tracert
        tracert = subprocess.Popen([f'tracert', '-d', address], shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)

        # Read the output
        lines = tracert.stdout.readlines()
        res = b"".join(lines).decode("utf-8", 'ignore')
        
        return re.findall(ipv4, res)[1:]
        
    except subprocess.SubprocessError as e:
        print(e)
        return []
    


def ping(hostname):
        """
        Ping the host and return the result
        host: The host to ping
        """
        time = date_now()
        try:
            # Run ping
            proccess = subprocess.Popen("ping "+hostname+" -n 1", shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            
            result = proccess.stdout.read().decode("utf-8", 'ignore')

            for line in result.splitlines():
                
                if re.search('.*tempo=([0-9]+)ms.*', line) is not None:
                    rtt = re.findall('.*tempo=([0-9]+)ms.*', line)[0]
                    ttl = re.findall('.*TTL=([0-9]+).*', line)[0]

                elif re.search('.*time=([0-9]+)ms.*', line) is not None:
                    rtt = re.findall('.*time=([0-9]+)ms.*', line)[0]
                    ttl = re.findall('.*TTL=([0-9]+).*', line)[0]

                elif re.search('.*Request timed out.*', line) is not None:
                    rtt = -1
                    ttl = -1

                elif re.search('.*Esgotado o tempo limite do pedido.*', line) is not None:
                    rtt = -1
                    ttl = -1
            
            return [time, hostname, rtt, ttl]

        except Exception as e:
            print(e)
            return [time, hostname, -1, -1]
        
    

def write_log(path: str, value: list):
    """
    Write the log
    """
    while True:
        try:
            with open(f'.\\logs\\{path}.log', 'a') as f:
                f.write(f'{value[0]},{value[1]},{value[2]},{value[3]}\n')
            break
        
        except Exception as e:
            print(e)
            time.sleep(1)
            continue



def read_file(path: str):
    """
    Read the file
    """
    time = []
    host = 0
    rtts = []
    ttl = 0
    try:
        with open(f'.\\logs\\{path}.log', 'r') as f:
            f = f.readlines()
            for line in f:
                line = line.split(',')
                time.append(line[0])
                host = line[1]
                rtts.append(line[2])
                ttl = line[3]
                
            return [time, host, rtts, ttl]

                                        
    except FileNotFoundError:
        print(f'{path} not found!')

        return [time, host, rtts, ttl]  


class Calculate:
    def __init__(self, rtts: list):
        """ 
        Initialize the class
        line: file
        Set Rtts
        return: packet_sent, packet_recv, loss, rtt_best, rtt_avrg, rtt_worst, rtts, jitter, jitter_best, jitter_avrg, jitter_worst
        """
 
        self.rtt = rtts
 

    def __calc_latency(self, rtts: list):
        """ 
        Calculate value Latency
        best = min(rtts) 
        avrg = sum(rtts) / len(rtts) 
        worst = max(rtts) 
        return: rtt_best, rtt_avrg, rtt_worst
        """
        if len(rtts) >= 2:
            # Calculate Latency
            best = min(rtts) # Latency min
            avrg = sum(rtts) / len(rtts) # Latency avg
            worst = max(rtts) # Latency max
        else:
            best = 0
            avrg = 0
            worst = 0

        return [float('{:.3f}'.format(best)), float('{:.3f}'.format(avrg)), float('{:.3f}'.format(worst))]


    def __calc_loss(self, sent: int, recv: int):
        """
        Calculate value Loss
        loss = (sent - recv) / sent * 100 # loss in %
        return: packet_sent, packet_recv, loss
        """
        try:
            # Calculate Loss
            loss = (sent - recv) / sent * 100 # loss
        
        except ZeroDivisionError:
            loss = 0

        return [sent, recv, float('{:.3f}'.format(abs(loss)))]


    def __calc_jitter(self, rtts: list):
        """
        Calculate value Jitter with rtt
        l1 - l2 = j
        l2 - l3 = j
        return: jitter, jitter_best, jitter_avrg, jitter_worst
        """
        # Variables ambiente
        res_jitter = []

        # Navegar entre os valores da lista
        for i in range(len(rtts)):
            try:
                # Calculando jitter
                a = rtts[i] - rtts[i+1]
                # Add values from Dict
                res_jitter.append(float('{:.3f}'.format(abs(a))))

            except IndexError:
                    continue
        
        if len(res_jitter) >= 2:
            # Calculate Jitter
            best = min(res_jitter) # Latency min
            avrg = sum(res_jitter)/len(res_jitter) # Latency avg
            worst = max(res_jitter) # Latency max
            
        else:
            best = 0
            avrg = 0
            worst = 0
            res_jitter = [0]
        
        return [res_jitter, float('{:.3f}'.format(best)), float('{:.3f}'.format(avrg)), float('{:.3f}'.format(worst))]


    def __recv_rtts(self):
        # Return rtts
        rtts = []
        for i in self.rtt:
            if str(i) != '-1':
                rtts.append(float(i))

        return rtts

    def __packet_sent(self):
        # Return packet sent
        return (len(self.rtt))

    def __packet_recv(self):
        # Return packet recv
        return (len(self.__recv_rtts()))


    def calc_rtts(self):
        """
        return: rtt_best, rtt_avrg, rtt_worst
        """
        # Result Latency
        return self.__calc_latency(self.__recv_rtts())
    
    def calc_loss(self):
        """
        return: packet_sent, packet_recv, loss
        """
        # Result Loss
        return self.__calc_loss(self.__packet_sent(), self.__packet_recv())

    def calc_jitter(self):
        """
        return: jitter, jitter_best, jitter_avrg, jitter_worst
        """
        # Result Jitter
        return self.__calc_jitter(self.__recv_rtts())


def public_IP():
    return requests.get('http://meuip.com/api/meuip.php').text
        

def gateway_IP():
    pass


def local_IP():
    return socket.gethostbyname(socket.gethostname())
    

if __name__ == '__main__':
    print(read_file('proxy7.idtbrasilhosted.com'))
