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

        try:
          self.icon = PhotoImage(file=r"favicon.ico")
          self.tela.tk.call('wm', 'iconphoto', self.tela._w, self.icon)
        except:
            pass

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
        self.filemenu1.add_command(label="Abrir (Ctrl + O)", command=self.perguntar_salvar)
        self.tela.bind("<Control-o>", self.perguntar_salvar)
        self.filemenu1.add_command(label="Salvar (Ctrl + S)", command=self.salvar_em_arquivo)
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
        self.mainmenu.add_cascade(label="Editar", menu=self.filemenu2)

        self.filemenu3.add_command(label="Run (F5)", command=self.rodarCodigo)
        self.tela.bind("<Control-f>", '<F5>', self.rodarCodigo)
        self.mainmenu.add_cascade(label="Rodar", menu=self.filemenu3)

        self.filemenu4.add_command(label="Documentação", command=self.abrirDocumentacao)
        self.mainmenu.add_cascade(label="Ajuda", menu=self.filemenu4)

        self.opcaoEncontrar = False
        self.opcaoTelaPython = True
        self.exibirTela()

    def exibirTela(self):
        print('Classe:App - exibirTela')
        self.editor.exibirTela()
        self.editorPy.exibirTela(self.editor)
        self.tela.config(menu=self.mainmenu)

    def ocultarTela(self):
        print('Classe:App - ocultarTela')
        self.editor.ocultarTela()

    def abrirDocumentacao(self, event = None):
        conteudo_html = """<!DOCTYPE html>
<html>

<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
      margin: 0;
      padding: 20px;
    }

    h1 {
      color: #333;
    }

    p {
      margin: 10px 0;
    }

    code {
      background-color: #f5f5f5;
      padding: 2px 6px;
      border: 1px solid #ccc;
    }

    .section {
      background-color: #fff;
      border: 1px solid #ccc;
      padding: 20px;
      margin: 10px 0;
      border-radius: 5px;
    }

    .code-example {
      background-color: #f5f5f5;
      padding: 10px;
      border: 1px solid #ccc;
      margin: 10px 0;
    }
  </style>
</head>

<body>
  <h1>Documentação Básica</h1>

  <div class="section">
    <h2>Proposta PortuPy</h2>
    <p>
      O PortuPy é uma pseudolinguagem que foi
      criada com o propósito de ensinar os conceitos fundamentais da programação de uma forma divertida e acessível,
      especialmente para estudantes iniciantes.
    </p>
    <p>
      PortuPy tem sua sintaxe semelhante a do Python (linguagem de programação real, muito usada no mercado).
      O objetivo do uso dessa pseudolinguagem é que futuramente o aluno progride para uma linguagem de programação,
      nesse caso, preferenciamento, o Python, pela sua facilidade de aprendizado. Essa ferramenta usa palavras em
      português para representar comandos de programação, o que o torna mais acessível para pessoas
      que falam a língua portuguesa. Isso é ótimo para iniciantes, pois elimina a barreira do idioma.
    </p>
    <p>
      Além disso, mesmo sendo uma pseudolinguagem, o PortuPy é projetado para ensinar conceitos fundamentais de
      programação, como variáveis, estruturas condicionais, loops e funções. Os estudantes podem aprender esses
      conceitos de forma interativa e prática.
    </p>
    <p>
      Em resumo, o PortuPy é uma pseudolinguagem de programação que se destaca por sua simplicidade e acessibilidade.
      Ele é uma ferramenta valiosa para aqueles que estão dando os primeiros passos na programação e desejam entender os
      conceitos básicos de uma forma amigável e envolvente. Se você está começando a estudar programação, o PortuPy pode
      ser uma introdução divertida e educativa a este mundo fascinante.
    </p>
  </div>

  <div class="section">
    <h2>Comandos de Entrada e Saída</h2>
    <p>Para receber entrada do usuário em PortuPy, você pode usar a função <code>entrada()</code>:</p>
    <div class="code-example">
      <pre>
nome = entrada("Digite seu nome: ")
      </pre>
    </div>
    <p>Para exibir saída, use a função <code>escrever()</code>:</p>
    <div class="code-example">
      <pre>
escrever("Olá, " + nome)
      </pre>
    </div>
  </div>

  <div class="section">
    <h2>Principais Tipos de Dados</h2>
    <p>Python suporta diversos tipos de dados, incluindo:</p>
    <ul>
      <li>Números inteiros (inteiro)</li>
      <li>Números decimais (decimal)</li>
      <li>Carateres (caracter)</li>
      <li>Lógicos (logico)</li>
    </ul>
    <div class="code-example">
      <pre>
#caracter
nome = "Joao"

#inteiro
idade = 15

#decimal
altura = 1.75

#logico
trabalha = Verdadeiro
      </pre>
    </div>
  </div>

  <div class="section">
    <h1>Operadores em PortuPy</h1>

    <div class="section">
      <h2>Operadores Aritméticos</h2>
      <ul>
        <li><code>+</code> (Adição)</li>
        <li><code>-</code> (Subtração)</li>
        <li><code>*</code> (Multiplicação)</li>
        <li><code>/</code> (Divisão)</li>
        <li><code>//</code> (Divisão de Piso)</li>
        <li><code>%</code> (Módulo - Resto da Divisão)</li>
        <li><code>**</code> (Exponenciação)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operadores de Comparação</h2>
      <ul>
        <li><code>==</code> (Igual a)</li>
        <li><code>!=</code> (Diferente de)</li>
        <li><code>&lt;</code> (Menor que)</li>
        <li><code>&gt;</code> (Maior que)</li>
        <li><code>&lt;=</code> (Menor ou igual a)</li>
        <li><code>&gt;=</code> (Maior ou igual a)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operadores Lógicos</h2>
      <ul>
        <li><code>and</code> (E lógico)</li>
        <li><code>or</code> (Ou lógico)</li>
        <li><code>not</code> (Negação lógica)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operadores de Identidade</h2>
      <ul>
        <li><code>is</code> (É)</li>
        <li><code>is not</code> (Não é)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operadores de Associação</h2>
      <ul>
        <li><code>in</code> (Está em)</li>
        <li><code>not in</code> (Não está em)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operadores de Atribuição</h2>
      <ul>
        <li><code>=</code> (Atribuição)</li>
        <li><code>+=</code> (Adição e atribuição)</li>
        <li><code>-=</code> (Subtração e atribuição)</li>
        <li><code>*=</code> (Multiplicação e atribuição)</li>
        <li><code>/=</code> (Divisão e atribuição)</li>
        <li><code>%=</code> (Módulo e atribuição)</li>
        <li><code>//=</code> (Divisão de Piso e atribuição)</li>
        <li><code>**=</code> (Exponenciação e atribuição)</li>
      </ul>
    </div>

    <div class="section">
      <h2>Operador de Concatenação de Strings</h2>
      <ul>
        <li><code>+</code> (Usado para concatenar strings)</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h1>Entendendo Estruturas de Condição</h1>

    <p>As estruturas de condição são usadas para criar lógica condicional em programas. Elas permitem que você tome
      decisões com base em condições específicas.</p>

    <h2>Exemplo de Estrutura de Condição:</h2>
    <div class="code-example">
      <pre>
# Solicita ao usuário que insira um número
numero = decimal(entrada("Digite um número: "))

# Verifica se o número é positivo
se numero > 0:
    escrever("O número é positivo.")
e se numero == 0:
    escrever("O número é zero.")
senao:
    escrever("O número é negativo.")

        </pre>
    </div>

    <p>Neste exemplo em Python, estamos verificando se a variável <code>idade</code> é maior ou igual a 18. Se a
      condição for verdadeira, o programa imprime "Você é maior de idade". Caso contrário, ele imprime "Você é menor de
      idade".</p>

    <h2>Principais Estruturas de Condição:</h2>
    <ul>
      <li><strong>se</strong>: Usado para verificar se uma condição é verdadeira.</li>
      <li><strong>e se</strong>: Permite verificar várias condições.</li>
      <li><strong>senao</strong>: Fornece uma alternativa caso a condição do <strong>if</strong> seja falsa.</li>
    </ul>

    <p>As estruturas de condição são fundamentais para criar programas que podem se adaptar a diferentes situações e
      tomar decisões com base em informações variáveis.</p>

  </div>

  <div class="section">
    <h1>Entendendo Estruturas de Repetição</h1>

    <p>As estruturas de repetição são usadas para executar um bloco de código várias vezes. Elas são essenciais para
      automatizar tarefas repetitivas em programas.</p>

    <h2>Estrutura de Repetição <code>para</code>:</h2>
    <div class="code-example">
      <pre>
nomes = ["Alice", "Bob", "Carol", "David"]
para nome em nomes:
    escrever("Olá, " + nome)
        </pre>
      <pre>
para x em faixa(10):
    escrever(x)
        </pre>
    </div>

    <p>Neste exemplo em Python, usamos um loop <code>para</code> para percorrer a lista de nomes e imprimir uma saudação
      para cada pessoa na lista.</p>

    <h2>Estrutura de Repetição <code>enquanto</code>:</h2>
    <div class="code-example">
      <pre>
contador = 0

enquanto contador &lt; 5:
    escrever("Contagem: " + caracter(contador))
    contador += 1
        </pre>
    </div>

    <p>Neste exemplo, usamos um loop <code>enquanto</code> para contar de 0 a 4. O loop continuará executando até que a
      condição <code>contador &lt; 5</code> seja falsa.</p>

    <p>As estruturas de repetição são cruciais para a automação e repetição de tarefas em programas, economizando tempo
      e esforço.</p>

  </div>
  <div class="section">
    <h1>Funções em Programação</h1>

    <p>Funções são blocos de código que podem ser reutilizados para realizar tarefas específicas. Elas ajudam a organizar e modularizar um programa.</p>

    <h2>Definindo e Chamando Funções:</h2>
    <div class="code-example">
        <pre>
# Definindo uma função
funcao saudacao(nome):
    devolva "Olá, " + nome

# Chamando a função
mensagem = saudacao("Alice")
escrever(mensagem)
        </pre>
    </div>

    <p>Neste exemplo em PortuPy, definimos uma função chamada `saudacao` que aceita um argumento `nome` e retorna uma mensagem de saudação. Em seguida, chamamos a função e armazenamos a mensagem resultante em uma variável.</p>

    <h2>Funções com Parâmetros Opcionais:</h2>
    <div class="code-example">
        <pre>
# Função com parâmetro opcional
funcao boas_vindas(nome, cidade="Desconhecida"):
    return "Olá, " + nome + " de " + cidade

# Chamando a função
mensagem = boas_vindas("Bob")
escrever(mensagem)
        </pre>
    </div>

    <p>Neste exemplo, a função `boas_vindas` aceita dois parâmetros, sendo que `cidade` tem um valor padrão opcional. Se a cidade não for fornecida, ela será definida como "Desconhecida" por padrão.</p>

    <p>As funções são uma parte fundamental da programação, permitindo a criação de blocos de código reutilizáveis para executar tarefas específicas.</p>

  </div>
</body>

</html>"""

        # Crie um arquivo HTML temporário
        with open("documentacao.html", "w", encoding="utf-8") as html_file:
            html_file.write(conteudo_html)

        # Abra o arquivo no navegador padrão
        webbrowser.open("documentacao.html")

    def codificarParaPortoPy(self, event = None, *args):
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

    def abrirOpcaoEncontrar(self, event = None):
        print('Classe:App - abrirOpcaoEncontrar')
        self.opcaoEncontrar = False if self.opcaoEncontrar else True
        self.encontrar.exibirTela(self.editor) if self.opcaoEncontrar else self.encontrar.ocultarTela()

    def abrirOpcaoTelaPython(self, event = None):
        print('Classe:App - abrirOpcaoTelaPython')
        self.opcaoTelaPython = False if self.opcaoTelaPython else True
        self.editorPy.exibirTela(self.editor) if self.opcaoTelaPython else self.editorPy.ocultarTela()

    def salvar_em_arquivo(self, event = None):
        print('Classe:App - salvar_em_arquivo')
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

    def perguntar_salvar(self, event = None):
        print('Classe:App - perguntar_salvar')
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
        print('Classe:App - abrir_arquivo')
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
        print('Classe:App - fechar_janela')
        if not self.arquivoSalvo:
            resposta = messagebox.askyesnocancel("Salvar Alterações?", "Deseja salvar as alterações?")
            if resposta is None:
                return
            elif resposta:
                self.salvar_em_arquivo()
            self.tela.destroy()
        else:
            self.tela.destroy()
    def rodarCodigo(self, event = None):
        print('Classe:App - rodarCodigo')
        codigo = self.editor.text.get("1.0", "end-1c")
        resultado = self.decodificador.codificadorParaPython(codigo)
        mensagem = self.run.runCod(resultado)
        if mensagem and mensagem[0] == 'erro':
            if len(mensagem) >= 3:
              self.editor.add_underline(mensagem[2])
            messagebox.showerror('titulo', mensagem[1])

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
