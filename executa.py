# -*- coding: utf-8 -*-
#!/usr/bin/env python
import thread # should use the threading module instead!
import pika
import time
import timeit
import uuid
import os
from threading import Thread
import base64
import subprocess
from tkinter import *
from tkFileDialog import askopenfilename

class Recieve(Thread):

    def on_request(self, ch, method, props, body):

        filename = ''
        imgdata = ""

        if body.find(".txt") > 0:

            file = body[::-1]
            body, rest = file.split('/', 1)
            print(body)
            file = body[::-1]

            arq = open("Server_peer/.recebidos.txt", "w")
            filename = 'Server_peer/.'+file 
            arq.write(filename)
            arq.close()
        else:
            imgdata = base64.b64decode(body)
            
            arq = open("Server_peer/.recebidos.txt", "r")
            filename = arq.read()
            arq.close()
            
            with open(filename, 'wb') as f:
                f.write(imgdata)
            print(filename)

        response = "deu certo"
        print(response)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        url = os.environ.get('tkxllkea', 'amqp://popzhidh:Oqlcsw9vbHel4zMcZbTQv2z7sH0ZoNxG@spider.rmq.cloudamqp.com/popzhidh')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel() # start a channel
        channel.queue_declare(queue='rpc_queue')
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.on_request, queue='rpc_queue')

        print(" [x] Awaiting RPC requests")
        channel.start_consuming()

	def fib():
	    arq = open("str.txt", "w")
	    str = None
	    with open("/home/douglas/Documentos/Trabalho_sd/oi.txt", "rb") as imageFile:
	        str = base64.b64encode(imageFile.read())
	    arq.write(str)
	    arq.close()

	    arq = open("str.txt", "r")
	    string = arq.read()
	    print(string)
	    arq.close()
	    return string

class Application:
	def __init__(self, master=None):
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

		self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()

		self.nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
		self.nomeLabel.pack(side=LEFT)

		self.nome = Entry(self.segundoContainer)
		self.nome["width"] = 30
		self.nome["font"] = self.fontePadrao
		self.nome.pack(side=LEFT)

		self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
		self.senhaLabel.pack(side=LEFT)

		self.senha = Entry(self.terceiroContainer)
		self.senha["width"] = 30
		self.senha["font"] = self.fontePadrao
		self.senha["show"] = "*"
		self.senha.pack(side=LEFT)

		self.autenticar = Button(self.quartoContainer)
		self.autenticar["text"] = "Autenticar"
		self.autenticar["font"] = ("Calibri", "8")
		self.autenticar["width"] = 12
		self.autenticar["command"] = self.verificaSenha
		self.autenticar.pack()

		self.autenticar = Button(self.quartoContainer)
		self.autenticar["text"] = "Cadastre-se"
		self.autenticar["font"] = ("Calibri", "8")
		self.autenticar["width"] = 12
		self.autenticar["command"] = self.cadastrar
		self.autenticar.pack()

		self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

	#Método verificar senha
	def verificaSenha(self):
		toserver = Send(self.nome.get()+'\n'+self.senha.get())
		oi = toserver.run()
		if oi == "acerto mizeravi":
			inicio.destroy()
			b.start()
			main = Tk()
			Main(main)
			main.mainloop()
		else:
			print("errou")

	def cadastrar(self):
		cadastrar = Tk()
		Cadastrar(cadastrar)
		cadastrar.mainloop()

class Cadastrar:

	def __init__(self, master=None):
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
		self.quartoContainer["padx"] = 20
		self.quartoContainer.pack()

		self.quintoContainer = Frame(master)
		self.quintoContainer["pady"] = 20
		self.quintoContainer.pack()

		self.titulo = Label(self.primeiroContainer, text="Cadastre-se")
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()

		self.nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
		self.nomeLabel.pack(side=LEFT)

		self.nome = Entry(self.segundoContainer)
		self.nome["width"] = 30
		self.nome["font"] = self.fontePadrao
		self.nome.pack(side=LEFT)

		self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
		self.senhaLabel.pack(side=LEFT)

		self.senha = Entry(self.terceiroContainer)
		self.senha["width"] = 30
		self.senha["font"] = self.fontePadrao
		self.senha["show"] = "*"
		self.senha.pack(side=LEFT)

		self.senhaLabel = Label(self.quartoContainer, text="Confirmar\n Senha", font=self.fontePadrao)
		self.senhaLabel.pack(side=LEFT)

		self.csenha = Entry(self.quartoContainer)
		self.csenha["width"] = 30
		self.csenha["font"] = self.fontePadrao
		self.csenha["show"] = "*"
		self.csenha.pack(side=LEFT)

		self.autenticar = Button(self.quintoContainer)
		self.autenticar["text"] = "Cadastre-se"
		self.autenticar["font"] = ("Calibri", "8")
		self.autenticar["width"] = 12
		self.autenticar["command"] = self.cadastrar
		self.autenticar.pack()

		self.mensagem = Label(self.quintoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()


	def cadastrar(self):
		if self.senha.get()==self.csenha.get():
			cadastrar.destroy()
			Application(inicio)


class Main:

	def __init__(self, master=None):
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

		self.quintoContainer = Frame(master)
		self.quintoContainer["pady"] = 5
		self.quintoContainer.pack()

		self.titulo = Label(self.primeiroContainer, text="Bem-Vindo"+user)
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()

		self.envia = Button(self.quartoContainer)
		self.envia["text"] = "Enviar Arquivo"
		self.envia["font"] = ("Calibri", "8")
		self.envia["width"] = 12
		self.envia["command"] = self.send
		self.envia.pack()

		'''self.baixar = Button(self.quintoContainer)
		self.baixar["text"] = "Baixar Arquivo"
		self.baixar["font"] = ("Calibri", "8")
		self.baixar["width"] = 12
		self.baixar["command"] = self.download
		self.baixar.pack()'''

		self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

		self.mensagem = Label(self.quintoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

	def send(self):
		root = Tk()
		root.withdraw()
		file = askopenfilename()
		topeer = SendPeer(file)
		topeer2 = SendPeer(file)
		topeer3 = SendPeer(file)
		oi = topeer.start()
		oi = topeer2.start()
						
		print(oi)


class SendPeer(Thread):

    def __init__(self,num):
    	
        Thread.__init__(self)
        self.num = num
        result = channel1.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        channel1.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def run(self):
        print(" [x] Enviando2")
        toserver.call(self.num)

        stri = ""
        with open(self.num, "rb") as imageFile:
            stri = base64.b64encode(imageFile.read())
        print(stri)
        return toserver.call(stri)
        

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        channel1.basic_publish(exchange='',
                                   routing_key='rpc_peer',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            connection.process_data_events()
        return self.response


class Send(Thread):

    def __init__(self,num):

        Thread.__init__(self)
        self.num = num
        result = channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def run(self):
        print(" [x] Enviando1")
        print(self.num)
        return toserver.call(self.num)
        

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=msg)
        while self.response is None:
            connection.process_data_events()
        return self.response


url1 = os.environ.get('nfwwsnsc', 'amqp://nfwwsnsc:6q16k6MT2TnoQdnNq2FZwdbLJNPb2dNU@crocodile.rmq.cloudamqp.com/nfwwsnsc')
params1 = pika.URLParameters(url1)
connection1 = pika.BlockingConnection(params1)
channel1 = connection1.channel()

url = os.environ.get('tkxllkea', 'amqp://popzhidh:Oqlcsw9vbHel4zMcZbTQv2z7sH0ZoNxG@spider.rmq.cloudamqp.com/popzhidh')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

b = Recieve()
toserver = Send(None)
topeer = SendPeer(None)
user=""
cadastrar = Tk()
inicio = Tk()
Application(inicio)
inicio.mainloop()
