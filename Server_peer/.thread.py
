from Tkinter import *

import thread # should use the threading module instead!
import Queue

import os

class ThreadSafeConsole(Text):
    def run():
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Bem-Vindo")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.envia = Button(self.quartoContainer)
        self.envia["text"] = "Enviar Arquivo"
        self.envia["font"] = ("Calibri", "8")
        self.envia["width"] = 12
        self.envia["command"] = self.new
        self.envia.pack()

        self.baixar = Button(self.quartoContainer)
        self.baixar["text"] = "Baixar Arquivo"
        self.baixar["font"] = ("Calibri", "8")
        self.baixar["width"] = 12
        self.baixar["command"] = self.baixar
        self.baixar.pack()

        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        
    def new(self):
        pass

    def baixar(self):
        pass
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.insert(END, str(line))
                self.see(END)
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.update_me)

# this function pipes input to an widget
def pipeToWidget(input, widget):
    widget.clear()
    while 1:
        line = input.readline()
        if not line:
            break
        widget.write(line)

def funcThread(widget):
    input = os.popen('dir', 'r')
    pipeToWidget(input, widget)

# uber-main
root = Tk()
widget = ThreadSafeConsole(root)
widget.pack(side=TOP, expand=YES, fill=BOTH)
thread.start_new(widget.run, (widget,))
thread.start_new(funcThread, (widget,))
thread.start_new(funcThread, (widget,))
thread.start_new(funcThread, (widget,))
thread.start_new(funcThread, (widget,))