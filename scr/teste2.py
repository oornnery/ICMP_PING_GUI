import time
import threading
from datetime import datetime
from module.ICMP import Ping

threads = []
HOST_ATIVOS = []


class Pingthread(threading.Thread):
    def __init__(self, host, meuId, namefile, mutex):
        self.host = host
        self.meuId = meuId
        self.mutex = mutex
        self.namfile = namefile
        self.log_ping = f"logPing-{namefile}.log"
        self.log_error = f"logError-{namefile}.log"
        self.log_process = f"logProcess-{namefile}.log"

        threading.Thread.__init__(self)

    def timenow(self):
        return datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    
    def write_log(self, filename, data):
        with open(f'.//log//{filename}', 'a', encoding='utf-8') as f:
                f.write(f"{data}\n")

    def add_host(self, host):
        HOST_ATIVOS.append(host)

    def remove_host(self, host):
        HOST_ATIVOS.remove(host)

    def ping(self):
        for i in range(1):
            with self.mutex:
                ping = Ping().main(self.host)
                self.write_log(self.namfile, f"host={ping[0]}, time={self.time}, rtts={ping[1]}, ttl={ping[2]}")
                time.sleep(1)

    def run(self):
        """
        Ping hosts
        count: number of pings
        host_list: list of hosts
        namefile: name of file to save log
        """
        stdoutmutex = threading.Lock()

        for seq in range(self.count):
            for id, host in enumerate(HOST_ATIVOS):
                self.write_log(self.log_process, f'{self.timenow()} :: Starting thread {id} for host {host}')
                thread = Pingthread(host, id, self.log_ping, stdoutmutex)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
