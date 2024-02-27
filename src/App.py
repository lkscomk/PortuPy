from tkinter import *
from ttkbootstrap import Style
from Decodificador import Decodificador
from EncontrarSubstituir import EncontrarSubstituir
from ComponenteEditor import Editor
from Run import Maquina
import webbrowser
import sys
from tkinter import filedialog
from tkinter import messagebox
import base64

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
        self.tela.geometry('%dx%d+%d+%d' %
                           (self.largura, self.altura, self.posx, self.posy))
        self.arquivo = ''
        self.arquivoSalvo = True
        self.tela.title(f'PortuPy (beta - V.0.1) - Nenhum arquivo aberto')

        image_data = base64.b64decode('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')
        self.icon = PhotoImage(data=image_data)
        self.tela.tk.call('wm', 'iconphoto', self.tela._w, self.icon)

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
        self.filemenu4 = Menu(self.mainmenu)
        self.filemenu1.add_command(
            label="Abrir (Ctrl + O)", command=self.perguntar_salvar)
        self.tela.bind("<Control-o>", self.perguntar_salvar)
        self.filemenu1.add_command(
            label="Salvar (Ctrl + S)", command=self.salvar_em_arquivo)
        self.tela.bind("<Control-s>", self.salvar_em_arquivo)
        self.filemenu1.add_separator()
        self.filemenu1.add_command(label="Sair", command=sys.exit)
        self.mainmenu.add_cascade(label="Arquivo", menu=self.filemenu1)

        self.filemenu2.add_command(label="Procurar (Ctrl + F)", command=self.abrirOpcaoEncontrar)
        self.tela.bind("<Control-f>", self.abrirOpcaoEncontrar)
        self.filemenu2.add_command(label="Ocultar/Mostrar tela Python (Ctrl + D)", command=self.abrirOpcaoTelaPython)
        self.tela.bind("<Control-d>", self.abrirOpcaoTelaPython)
        self.filemenu2.add_command(label="Converter Para PortoPy (Ctrl + K)", command=self.codificarParaPortoPy)
        self.tela.bind("<Control-k>", self.codificarParaPortoPy)
        self.filemenu2.add_separator()
        self.filemenu2.add_command(label="Aumentar Fonte (Ctrl +)", command=self.aumentar_fonte)
        self.tela.bind("<Control-plus>", self.aumentar_fonte)
        self.filemenu2.add_command(label="Diminuir Fonte (Ctrl -)", command=self.diminuir_fonte)
        self.tela.bind("<Control-minus>", self.diminuir_fonte)
        self.filemenu2.add_command(label="Desfazer (Ctrl + Z)", command=self.desfazer)
        self.tela.bind("<Control-z>", self.desfazer)
        self.filemenu2.add_command(label="Refazer (Ctrl + Shitf + Z)", command=self.refazer)
        self.tela.bind("<Control-Shift-Z>", self.refazer)
        self.filemenu2.add_command(label="Ajustar Indentação (Ctrl + B)", command=self.ajustar_indentacao)
        self.tela.bind("<Control-b>", self.ajustar_indentacao)
        self.mainmenu.add_cascade(label="Editar", menu=self.filemenu2)

        self.filemenu3.add_command(label="Run (F5)", command=self.rodarCodigo)
        self.tela.bind("<F5>", self.rodarCodigo)
        self.mainmenu.add_cascade(label="Rodar", menu=self.filemenu3)

        self.filemenu4.add_command(label="Documentação", command=self.abrirDocumentacao)
        self.mainmenu.add_cascade(label="Ajuda", menu=self.filemenu4)

        self.opcaoEncontrar = False
        self.opcaoTelaPython = True
        self.exibirTela()

    def ajustar_indentacao(self, event=None):
        codigo = self.editorPy.ajustar_indentacao(self.editorPy.text.get("1.0", "end-1c"))
        print(codigo)
        self.editorPy.text.delete("1.0", "end-1c")
        self.editorPy.text.insert(END, codigo)
        self.codificarParaPortoPy()

    def desfazer(self, event=None):
        self.editor.desfazer()
        self.editorPy.desfazer()

    def refazer(self, event=None):
        self.editor.refazer()
        self.editorPy.refazer()

    def aumentar_fonte(self, event=None):
        self.editor.aumentar_fonte()
        self.editorPy.aumentar_fonte()

    def diminuir_fonte(self, event=None):
        self.editor.diminuir_fonte()
        self.editorPy.diminuir_fonte()

    def exibirTela(self):
        print('Classe:App - exibirTela')
        self.editor.exibirTela()
        self.editorPy.exibirTela(self.editor)
        self.tela.config(menu=self.mainmenu)

    def abrirDocumentacao(self, event=None):
        webbrowser.open("https://portupy-view-2b443cd7e76d.herokuapp.com/#documentacao")

    def codificarParaPortoPy(self, event=None, *args):
        print('Classe:App - codificarParaPortoPy')
        self.editorPy.text.edit_modified(0)
        codigo = self.editorPy.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificarParaPortoPy(codigo)
        self.controladorEditor = False
        self.editor.text.delete("1.0", "end-1c")
        self.editor.text.insert(END, resultado)

    def codificarParaPython(self, *args):
        print('Classe:App - codificarParaPython')
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

    def abrirOpcaoEncontrar(self, event=None):
        print('Classe:App - abrirOpcaoEncontrar')
        self.opcaoEncontrar = False if self.opcaoEncontrar else True
        self.encontrar.exibirTela(self.editor) if self.opcaoEncontrar else self.encontrar.ocultarTela()

    def abrirOpcaoTelaPython(self, event=None):
        print('Classe:App - abrirOpcaoTelaPython')
        self.opcaoTelaPython = False if self.opcaoTelaPython else True
        self.editorPy.exibirTela(self.editor) if self.opcaoTelaPython else self.editorPy.ocultarTela()

    def salvar_em_arquivo(self, event=None):
        print('Classe:App - salvar_em_arquivo')
        conteudo = self.editor.text.get("1.0", "end-1c")

        # Abre uma caixa de diálogo para escolher o nome do arquivo
        if not self.arquivo:
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
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

    def perguntar_salvar(self, event=None):
        print('Classe:App - perguntar_salvar')
        if not self.arquivoSalvo:
            resposta = messagebox.askyesnocancel(
                "Salvar Alterações?", "Deseja salvar as alterações?")
            if resposta is None:
                return
            elif resposta:
                self.salvar_em_arquivo()
            self.abrir_arquivo()
        else:
            self.abrir_arquivo()

    def abrir_arquivo(self):
        print('Classe:App - abrir_arquivo')
        nome_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de Texto", "*.txt")])
        if nome_arquivo:
            self.editor.text.delete("1.0", "end-1c")
            with open(nome_arquivo, "r") as arquivo:
                conteudo = arquivo.read()
                self.editor.text.insert("end", conteudo)
            self.arquivo = nome_arquivo
            self.tela.title(f'PortuPy (beta - V.0.1) - {str(self.arquivo)}')
        self.arquivoSalvo = True

    def fechar_janela(self):
        print('Classe:App - fechar_janela')
        if not self.arquivoSalvo:
            resposta = messagebox.askyesnocancel(
                "Salvar Alterações?", "Deseja salvar as alterações?")
            if resposta is None:
                return
            elif resposta:
                self.salvar_em_arquivo()
            self.tela.destroy()
        else:
            self.tela.destroy()

    def rodarCodigo(self, event=None):
        print('Classe:App - rodarCodigo')
        codigo = self.editor.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificadorParaPython(codigo)
        mensagem = self.run.runCod(resultado)
        if mensagem and mensagem[0] == 'erro':
            if len(mensagem) >= 3:
                self.editor.add_underline(mensagem[2])
            messagebox.showerror('Ops... Algum Problema foi encontrado!', mensagem[1])

    def organizar_cores(self):
        print('Classe:App - organizar_cores')

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
    tela = App(root)
    tela.exibirTela()
    root.mainloop()
