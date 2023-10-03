from tkinter import *
from ttkbootstrap import Style
from Decodificador import Decodificador
from EncontrarSubstituir import EncontrarSubstituir
from ComponenteEditor import Editor
from Run import Maquina
import sys
from tkinter import font, filedialog
from tkinter import messagebox
from tkinter import messagebox as mbox




class App:
    def __init__(self, master=None):
        self.tela = master
        self.tela.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.largura = 1360
        self.altura = 768

        # resoução screen
        self.largura_screen = self.tela.winfo_screenwidth()
        self.altura_screen = self.tela.winfo_screenheight()

        # posição
        self.posx = self.largura_screen / 2 - self.largura / 2
        self.posy = self.altura_screen / 2 - self.altura / 2

        self.tela.minsize(500, 500)
        # master.state('zoomed')
        self.tela.geometry('%dx%d+%d+%d' % (self.largura, self.altura, self.posx, self.posy))
        self.arquivo = ''
        self.arquivoSalvo = True
        self.tela.title(f'PortuPy (beta - V.0.1) - Nenhum arquivo aberto')

        self.editor = Editor(master)
        self.editorPy = Editor(master)
        self.encontrar = EncontrarSubstituir(master, self.editor.text)
        self.decodificador = Decodificador()
        self.run = Maquina()

        self.editor.text.bind('<<Modified>>', self.codificarParaPython)

        self.cor_de_tela = None
        self.cor_primaria = None
        self.cor_segundaria = None
        self.cor_danger = None
        self.cor_inputfg = None
        self.cor_success = None
        self.font_padrao = ('helvetica', 9)
        self.organizar_cores()

        self.mainmenu = Menu(master)
        self.filemenu1 = Menu(self.mainmenu)
        self.filemenu2 = Menu(self.mainmenu)
        self.filemenu3 = Menu(self.mainmenu)
        self.filemenu1.add_command(label="Abrir", command=self.perguntar_salvar)
        self.filemenu1.add_command(label="Salvar", command=self.salvar_em_arquivo)
        self.filemenu1.add_separator()
        self.filemenu1.add_command(label="Sair", command=sys.exit)
        self.mainmenu.add_cascade(label="Arquivo", menu=self.filemenu1)

        self.filemenu2.add_command(label="Procurar", command=self.abrirOpcaoEncontrar)
        self.filemenu2.add_command(label="Ocultar/Mostrar tela Python", command=self.abrirOpcaoTelaPython)
        self.filemenu2.add_command(label="Converter Para PortoPy", command=self.codificarParaPortoPy)
        self.filemenu2.add_separator()
        self.mainmenu.add_cascade(label="Editar", menu=self.filemenu2)

        self.filemenu3.add_command(label="Run", command=self.rodarCodigo)
        # self.filemenu3.add_separator()
        self.mainmenu.add_cascade(label="Run", menu=self.filemenu3)

        self.opcaoEncontrar = False
        self.opcaoTelaPython = True
        self.exibirTela()

    def exibirTela(self):
        print('Classe:Login - exibirTela')
        self.editor.exibirTela()
        self.editorPy.exibirTela(self.editor)
        self.tela.config(menu=self.mainmenu)

    def ocultarTela(self):
        print('Classe:Login - ocultarTela')
        self.editor.ocultarTela()

    def codificarParaPortoPy(self, *args):
        self.editorPy.text.edit_modified(0)
        codigo = self.editorPy.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificarParaPortoPy(codigo)
        self.controladorEditor = False
        self.editor.text.delete("1.0", "end-1c")
        self.editor.text.insert(END, resultado)

    def codificarParaPython(self, *args):
        self.editor.text.edit_modified(0)
        codigo = self.editor.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificadorParaPython(codigo)
        self.controladorEditor = True
        self.editorPy.text.delete("1.0", "end-1c")
        self.editorPy.text.insert(END, resultado)
        self.editor.remove_underline()
        if not self.arquivoSalvo:
            self.tela.title(f'*PortuPy (beta - V.0.1) - {str(self.arquivo)}* ')
        self.arquivoSalvo = False

    def abrirOpcaoEncontrar(self):
        self.opcaoEncontrar = False if self.opcaoEncontrar else True
        self.encontrar.exibirTela(self.editor) if self.opcaoEncontrar else self.encontrar.ocultarTela()

    def abrirOpcaoTelaPython(self):
        self.opcaoTelaPython = False if self.opcaoTelaPython else True
        self.editorPy.exibirTela(self.editor) if self.opcaoTelaPython else self.editorPy.ocultarTela()

    def salvar_em_arquivo(self):
      conteudo = self.editor.text.get("1.0", "end-1c")

      # Abre uma caixa de diálogo para escolher o nome do arquivo
      if not self.arquivo:
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
      else:
        nome_arquivo = self.arquivo

      if nome_arquivo:
          with open(nome_arquivo, "w") as arquivo:
              arquivo.write(conteudo)
          self.arquivo = nome_arquivo
          self.arquivoSalvo = True
          self.tela.title(f'PortuPy (beta - V.0.1) - {str(self.arquivo)}')
      else:
          print("Nenhum arquivo selecionado.")

    def perguntar_salvar(self):
        if not self.arquivoSalvo:
            resposta = messagebox.askyesnocancel("Salvar Alterações?", "Deseja salvar as alterações?")
            if resposta is None:
                return
            elif resposta:
                self.salvar_em_arquivo()
            self.abrir_arquivo()
        else:
            self.abrir_arquivo()

    def abrir_arquivo(self):
        nome_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if nome_arquivo:
            self.editor.text.delete("1.0", "end-1c")
            with open(nome_arquivo, "r") as arquivo:
                conteudo = arquivo.read()
                self.editor.text.insert("end", conteudo)
            self.arquivo = nome_arquivo
            self.tela.title(f'PortuPy (beta - V.0.1) - {str(self.arquivo)}')
        self.arquivoSalvo = True

    def fechar_janela(self):
        if not self.arquivoSalvo:
            resposta = messagebox.askyesnocancel("Salvar Alterações?", "Deseja salvar as alterações?")
            if resposta is None:
                return
            elif resposta:
                self.salvar_em_arquivo()
            self.tela.destroy()
        else:
            self.tela.destroy()
    def rodarCodigo(self):
        codigo = self.editor.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificadorParaPython(codigo)
        mensagem = self.run.runCod(resultado)
        if mensagem and mensagem[0] == 'erro':
            if len(mensagem) >= 3:
              self.editor.add_underline(mensagem[2])
            messagebox.showerror('titulo', mensagem[1])

    def organizar_cores(self):
        print('Classe:Login - organizar_cores')

        self.style = Style()
        self.style.configure('TButton', font=self.font_padrao)

        self.cor_bg = self.style.colors.get('bg')
        self.cor_primary = self.style.colors.get('primary')
        self.cor_secondary = self.style.colors.get('secondary')
        self.cor_danger = self.style.colors.get('danger')
        self.cor_inputbg = self.style.colors.get('inputbg')
        self.cor_inputfg = self.style.colors.get('inputfg')
        self.cor_success = self.style.colors.get('success')

if __name__ == '__main__':
  root = Tk()
  tela = Ambiente(root)
  tela.exibirTela()
  root.mainloop()
