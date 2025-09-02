import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class CustomDialog:
    def __init__(self, parent, title="Mensagem", message="", icon=None, dialog_type="yesno"):
        """
        :param parent: janela pai (normalmente sua root)
        :param title: título da janela
        :param message: texto da mensagem
        :param icon: objeto PhotoImage
        :param dialog_type: "yesno" ou "error"
        """
        self.parent = parent
        self.title = title
        self.message = message
        self.icon = icon
        self.dialog_type = dialog_type
        self.resposta = None

    def show(self):
        """Exibe o diálogo e retorna 'Yes' ou 'No' (ou None se fechar)."""
        win = tb.Toplevel(self.parent)

        largura = 500
        altura = 150

        # resoução screen
        largura_screen = win.winfo_screenwidth()
        altura_screen = win.winfo_screenheight()

        # posição
        posx = largura_screen / 2 - largura / 2
        posy = altura_screen / 2 - altura / 2

        # master.state('zoomed')
        win.geometry('%dx%d+%d+%d' %
                           (largura, altura, posx, posy))

        win.title(self.title)
        win.resizable(False, False)
        win.transient(self.parent)      # fica acima da janela principal
        win.grab_set()                  # bloqueia interação com a janela principal

        if self.icon:
            win.iconphoto(False, self.icon)

        # Frame principal
        frame = tb.Frame(win, padding=15)
        frame.pack(fill=BOTH, expand=True)

        # Mensagem
        lbl_msg = tb.Label(frame, text=self.message, anchor=CENTER, font=("Segoe UI", 11))
        lbl_msg.pack(pady=10)

        # Botões de ação
        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=10)

        if self.dialog_type == "yesno":
            tb.Button(btn_frame, text="Sim", bootstyle=SUCCESS,
                      command=lambda: self._close(win, "Yes")).pack(side=LEFT, padx=5)
            tb.Button(btn_frame, text="Não", bootstyle=DANGER,
                      command=lambda: self._close(win, "No")).pack(side=LEFT, padx=5)

        elif self.dialog_type == "error":
            tb.Button(btn_frame, text="OK", bootstyle=DANGER,
                      command=lambda: self._close(win, "No")).pack(side=LEFT, padx=5)

        self.parent.wait_window(win)
        return self.resposta

    def _close(self, win, resposta):
        self.resposta = resposta
        win.destroy()
