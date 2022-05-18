from icmplib import ping
import threading, sys, re, time
from lib.tracert import Tracert
from lib.modules import timenow
from lib.dns import dns_resolver
from lib.Calculate import Calculate
from lib.update_json import write_file
from lib.Table import run_table


def logging(msg):
        """
        """
        print(f'[{timenow()}] :: {msg}\n')
    

class MultiPingRouter(object):
    def __init__(self):
        self.path = f".//scr//Config//mtrconfig.json"
        self.log = str

        self.data = {}


    def run_dns(self, host):
        """
        """
        return dns_resolver(host)


    def run_tracert(self, host) -> list:
        """
        """
        return Tracert().main(host)


    def create_data(self, hosts):
        """
        """
        # Criando meta dados
        for i in hosts:
            self.data.update({f"{i}": {"pct_sent": 0, "pct_recv": 0, "pct_loss": 0, "rtt_best": 0, "rtt_avrg": 0, "rtt_worst": 0, "rtts": [], "times": [],
            "jitter_best": 0, "jitter_avrg": 0, "jitter_worst": 0, "jitter": [], "ttl": 0}})
        
        write_file(self.log, self.data)

    def run_ping(self, host):
        """
        """
        return ping(host, count=1).rtts
    
    def update_data_ping(self, value, key):
        """
        """

        if value == []:
            self.data[key]["rtts"].append(-1.0)
        else:
            for x in value:
                self.data[key]["rtts"].append(('{:.3f}').format(x))

        self.data[key]["times"].append(timenow())


    def calculate_ping(self, rtts, key):
        """
        """
        calc = Calculate(rtts)

        # Update Rtt
        rtt = calc._calculate_rtts()
        self.data[key]["rtt_best"] = rtt[0]
        self.data[key]["rtt_avrg"] = rtt[1]
        self.data[key]["rtt_worst"] = rtt[2]
        
        # Update Loss
        loss = calc._calculate_loss()
        self.data[key]["pct_sent"] = loss[0]
        self.data[key]["pct_recv"] = loss[1]
        self.data[key]["pct_loss"] = loss[2]

        # Update Jitter
        jitter = calc._calculate_jitter()
        self.data[key]["jitter"] = jitter[0]
        self.data[key]["jitter_best"] = jitter[1]
        self.data[key]["jitter_avrg"] = jitter[2]
        self.data[key]["jitter_worst"] = jitter[3]


    def main(self, ipaddr, count):
        """
        Receber um IP 
        Calcular a rota
        adicionar em rota em lista de MTR ativos
        Criar meta dados
        Calcular ping para cada host da rota
        remover rota de lista de MTR ativos
        escrever dados em json
        continuar execuçao dos MTR ainda ativos
        """
        dns = self.run_dns(ipaddr)
        self.log = f".//log//mtr-{dns}.json"

        if dns is not None:
            logging(f"DNS: {dns}")
            logging(f"Calculate router: {dns}")
            hosts = self.run_tracert(dns)
        else:
            print("DNS não encontrado")

        if hosts is not None:
                logging(f"Create data: {hosts}")
                self.create_data(hosts)
        else:
            print("Rota não encontrada")

        logging(f"Run ping: {hosts}")
        
        for i in range(count):
            # Stating ping routers
            for k in hosts:
                # Run ping
                self.update_data_ping(self.run_ping(k), k)
                # Calculate ping
                self.calculate_ping(self.data[k]["rtts"], k)
                # Remove ping
            write_file(self.log, self.data)
            run_table(self.data)

    


if __name__ == '__main__':
    host = 'google.com'
    namefile = 'test1'
    # path ./icmp-env/Scripts/python.exe .\scr\MTR.py google.com teste1
    MultiPingRouter().main(sys.argv[1], int(sys.argv[2]))
 
