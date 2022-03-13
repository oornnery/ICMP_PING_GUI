"""
Criar modulo multiping
    1. Recebe os dados para o ping(Host: list, Qtd: Int, size: int)
    2. Criar for Qtd: Iniciar multiping para os host enviando 1 pacote.
    3. Armazenar os dados em um dict com cada host com ID começando em 0.
    3. Criar Threading.
    4. Chamar função calculate para descobrir o jitter e latencia de cada key na var dict.
    5. Gravar dados em um json file.
    6. Add valores em var para ser exibido na tela. 
    7. exibir valores na tela usando o prettytable.
"""
import time
import threading
from typing import Dict
from prettytable import PrettyTable
from icmplib import multiping
from icmplib import ICMPError
import os

class MultiPing():
    def __init__(self) -> None:
        # Var
        self.result_multiping = Dict
        self.var_field_table = ["ID", "Hostname", "Loss", "Sent", "Recv", "Last", "min_rtt", "avg_rtt", "max_rtt", "jitter"]
        self.var_row_table = Dict

    def run_multiping(self, hosts: list[str], qtd: int):
        """
        Args:
            hosts (list[str]): ['127.0.0.1', '::1']
            qtd (int): 10
        """        
        c = 1
        result = self.result_multiping
        
        # estanciando module
        hosts = multiping(hosts, count=1)
        
        # criando Dict 
        for key, host in enumerate(hosts):
            result.update({f'Host{key}': {
                'ID': [],
                'Host': [],
                'Loss': [],
                'Sent': [],
                'Recv': [],
                'Last': [],
                'Avg': [],
                'Best': [],
                'Wrst': [],
                'Jitter': []
            }})
                
        # Inciando ping para os host e add os valores no dict
        while qtd >= c:
            for key, host in enumerate(hosts):
                result[f'Host{key}']['ID'].update(f'{key}') 
                result[f'Host{key}']['Host'].update(f'{host}') 
                time.sleep(0.5)
            c+=1

    def write_dict(self):
        pass

    def run_threading(self):
        pass

    def calculate(self):
        pass

    def write_json(self):
        pass

    def echo_table(self):
        pass


if __name__ == "__main__":
    h = ['proxy2.idtbrasilhosted.com']
    q = 3
    run_multiping(h, q)
