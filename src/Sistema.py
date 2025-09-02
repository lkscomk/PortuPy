from datetime import *
from pathlib import Path
from time import strftime
import json
import requests
from os.path import dirname, join
import os

class Sistema:
    def __init__(self):
        self.data = self.criar_data()
        self.local_app = self.criar_local_app()
        self.pasta_do_app = self.criar_pasta_app()
        self.baixar_comandos()

    def criar_data(self):
        print('Classe:Sistema - criar_data')
        data_atual = str(date.today())
        dia = data_atual[8:10]
        mes = data_atual[5:7]
        ano = data_atual[0:4]
        return (dia + '/' + mes + '/' + ano)

    def criar_local_app(self):
        print('Classe:Sistema - criar_local_app')
        try: 
            base_dir = os.path.expanduser(r"~\AppData\Loyal\Pryograms")
            os.makedirs(base_dir, exist_ok=True)
            return base_dir
        except:
            return '/'

    
    def baixar_comandos(self):
        print('Classe:Sistema - baixar_comandos')
        if self.tem_internet():
            print("Conectado à internet...")
            url = "https://drive.usercontent.google.com/uc?id=1K-V66ltFFv6DWIVSaozpIVfjolflv5iB&authuser=0&export=download"

            # faz o download do conteúdo
            response = requests.get(url)

            # verifica se o download deu certo
            if response.status_code == 200:
                data = response.json()
                current_dir = dirname(__file__)
                file_path = join(current_dir, "./comandos.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("❌ Sem conexão com a internet")
        

    def criar_pasta_app(self):
        print('Classe:Sistema - criar_pasta_app')
        d = self.local_app + r'\PortuPy'
        Path(d).mkdir(exist_ok=True)
        return d

    def criar_hora(self):
        print('Classe:Sistema - criar_hora')
        a = strftime("%H:%M:%S")
        return str(a)
    
    def tem_internet(self, url="http://www.google.com", timeout=10):
        try:
            requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False


if __name__ == '__main__':
    sistema = Sistema()
    print(sistema.criar_local_app())
    print(sistema.criar_pasta_app())
    print(sistema.criar_hora())
