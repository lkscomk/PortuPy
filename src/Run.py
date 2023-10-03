import os
import tempfile
import re

class Maquina:
    def __init__(self):
        pass

    def criarArquivoTemporario(self, codigo):
        cod = codigo + """
import time
time.sleep(20)
print('O terminal fechará em 5 segundos')
time.sleep(5)
        """
        print(cod)
        arquivo_temporario = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        arquivo_temporario.write(cod.encode())
        arquivo_temporario.close()
        return arquivo_temporario.name

    def runCod(self, cod):
        arquivo_temp = self.criarArquivoTemporario(cod)
        try:
            resultado = os.system(f'python {arquivo_temp}')
            print(resultado)
            if resultado == -1073741510:
              return None
            if resultado != 0:
              try:
                  compile(cod, '<string>', 'exec')
                  return ['erro', f"Erro não identificado. Por favor, verifique o código e tente novamente."]
              except Exception as erro:
                  linha = self.extrair_primeira_ocorrencia(str(erro))
                  return ['erro', str(erro), linha]
            else:
                return None
        except Exception as erro:
            return ['erro', f"Erro: {erro}"]
        finally:
            os.remove(arquivo_temp)

    def extrair_primeira_ocorrencia(self, texto):
        padrao = r'line (\d+)'
        correspondencia = re.search(padrao, texto)
        if correspondencia:
            numero = int(correspondencia.group(1))
            return numero
        else:
            return None

if __name__ == '__main__':
    codigo_usuario = """
nome = input('nome:')
print(nome)
a = 5
b = 3
soma = a + b
print("A soma de", a, "e", b, "é:", soma)
"""

    run = Maquina()
    run.runCod(codigo_usuario)
