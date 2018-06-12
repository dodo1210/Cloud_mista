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
try:
	from tKinter import *
except ImportError:
	from tkinter import *
from tkFileDialog import askopenfilename
import Tkinter, Tkconstants, tkFileDialog

class Recieve(Thread):


    def on_request(self, ch, method, props, body):

        filename = ''
        imgdata = ""
        response = ""

        if "down" in body:

            arq = open('.posicao.txt','r')
            posicao = arq.read()
            arq.close()

            print(body[0])

            posi = int(posicao)
            eh = body[0]

            if eh!=posi:

                print(body)
                arq = open("Server_peer/.todownload.txt", "r")
                files = arq.readlines()
                arq.close()

                for f in files:
                    print(f)
                    oi,file = f.split("/",1)
                    erro,send = body.split("down",1)
                    print(file, "."+send)
                    if "."+send == file:
                        stri = ""
                        arquivo,erro = file.split("\n",1)
                        with open("Server_peer/"+file, "rb") as imageFile:
                            stri = base64.b64encode(imageFile.read())
                        l = list(stri)
                        l.pop(0)
                        print(l)
                        stri = ''.join(l)
                        response = arquivo+"@"+stri
                        break

        else:

            arq = open('.posicao.txt','r')
            posicao = arq.read()
            arq.close()

            print(body[0])

            posi = int(posicao)
            eh = body[0]

            if eh!=posi:

                if body.find(".txt") > 0 or body.find(".doc") > 0 or body.find(".docx") > 0 or body.find(".xls") > 0 or body.find(".xlsx") > 0 or body.find(".ppt") > 0 or body.find(".pptx") > 0 or body.find(".odt") > 0 or body.find(".odp") > 0 or body.find(".pdf") > 0 or body.find(".mp3") > 0 or body.find(".wav") > 0 or body.find(".ogg") > 0 or body.find(".mid") > 0 or body.find(".midi") > 0 or body.find(".sh") > 0 or body.find(".py") > 0 or body.find(".rb") > 0 or body.find(".c") > 0 or body.find(".cpp") > 0 or body.find(".js") > 0 or body.find(".java") > 0 or body.find(".go") > 0 or body.find(".png") > 0 or body.find(".jpg") > 0 or body.find(".gif") > 0 or body.find(".svg") > 0 or body.find(".xml") > 0 or body.find(".html") > 0 or body.find(".css") > 0 or body.find(".mp4") > 0 or body.find(".mkv") > 0 or body.find(".iso") > 0 or body.find(".rar") > 0 or body.find(".zip") > 0 :

                    file = body[::-1]
                    body, rest = file.split('/', 1)
                    print(body)
                    file = body[::-1]

                    arq = open("Server_peer/.recebidos.txt", "w")
                    filename = 'Server_peer/.'+file+"\n"  # I assume you have a way of picking unique filenames
                    arq.write(filename)
                    arq.close()

                    arq = open("Server_peer/.todownload.txt", "a")
                    filename = 'Server_peer/.'+file  # I assume you have a way of picking unique filenames
                    arq.write(filename+"\n")
                    arq.close()
                    response = "deu certo"
                else:
                    imgdata = base64.b64decode(body)
                    
                    arq = open("Server_peer/.recebidos.txt", "r")
                    filename = arq.read()
                    arq.close()

                    print(body)
                    
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

		

	#Método verificar senha
	def verificaSenha(self):
		toserver = Send(self.nome.get()+'\n'+self.senha.get())
		oi = toserver.run()
		if "acerto mizeravi" in oi:

			arq = open('.posicao.txt',"w")
			p, erro = oi.split("acerto mizeravi",1)
			print("dcfvgbh"+oi,p,erro)
			arq.write(p)
			arq.close()

			inicio.destroy()
			b.start()
			main = Tk()
			Main(main)
			main.mainloop()

		else:
			self.titulo = Label(self.quartoContainer, text="Senha ou usuário incorreto")
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()
            

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

		self.sextoContainer = Frame(master)
		self.sextoContainer["pady"] = 20
		self.sextoContainer.pack()

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
		if self.senha.get() != self.csenha.get():
			print("ghj")
			self.senhaLabel = Label(self.sextoContainer, text="Senhas diferentes.\n Verifique sua senha", font=self.fontePadrao)
			self.senhaLabel.pack(side=LEFT)
		else:
			toserver = Send("cad."+self.nome.get()+'\n'+self.senha.get())
			oi = toserver.run()
			if oi == "acerto mizeravi":
				self.senhaLabel = Label(self.sextoContainer, text="Usuário ou senha\n cadastrados", font=self.fontePadrao)
				self.senhaLabel.pack(side=LEFT)
			else:
				self.senhaLabel = Label(self.sextoContainer, text="Cadastro\n efetuado", font=self.fontePadrao)
				self.senhaLabel.pack(side=LEFT)


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
		self.quintoContainer["pady"] = 50
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

		arq = open("Client_peer/.tosend.txt", "r")
		self.string = arq.readlines()
		arq.close()

		scrollbar = Scrollbar(master)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.listbox = Listbox(master, yscrollcommand=scrollbar.set)
		cont = 0
		
		for s in self.string:
			self.listbox.insert(END, s)
			cont = cont+1
		self.listbox.bind('<<ListboxSelect>>',self.down)
		self.listbox.pack(fill=BOTH, expand=1)
		scrollbar.config(command=self.listbox.yview)
        

	def send(self):
		root = Tk()
		root.withdraw()
		file = askopenfilename()
		arquivo = file

		arq = open("Client_peer/.tosend.txt", "a")
		arq.write(file+"\n")
		arq.close()

		arq = open("Client_peer/.tosend.txt", "r")
		string = arq.readlines()
		arq.close()

		self.mensagem = Label(self.quintoContainer, text=string[len(string)-1], font=self.fontePadrao)
		self.mensagem.pack()

		'''self.download = Button(self.quintoContainer)
								self.download["text"] = "Download"
								self.download["font"] = ("Calibri", "8")
								self.download["width"] = 12
								self.download["command"] = self.down
								self.download.pack()'''


		topeer = SendPeer(arquivo)
		topeer2 = SendPeer(arquivo)
		topeer3 = SendPeer(arquivo)
		oi2 = topeer2.start()
		oi3 = topeer3.start()
		self.listbox.insert(END, arquivo+"\n")

	def down(self,evt):
		value=str((self.listbox.get(ACTIVE)))
		file = value[::-1]
		value, f = file.split("/",1)
		print(value)
		topeer = Download(value[::-1])
		topeer2 = Download(value[::-1])
		topeer3 = Download(value[::-1])	
		oi = topeer.run()
		oi2 = topeer2.run()
		oi3 = topeer3.run()
		print(oi,oi2,oi3)


class SendPeer(Thread):

    def __init__(self,num):
    	
        Thread.__init__(self)
        self.num = num
        result = channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def run(self):
        print(" [x] Enviando2")
        toserver.call(self.num)

        arq = open('.posicao.txt','r')
        posicao = arq.read()
        arq.close()

        print(posicao)

        stri = ""
        with open(self.num, "rb") as imageFile:
            stri = base64.b64encode(imageFile.read())
        print(stri)
        return toserver.call(posicao+stri)
        

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        channel.basic_publish(exchange='',
                                   routing_key='rpc_peer',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            connection.process_data_events()
        return self.response


class Download(Thread):

    def __init__(self,num):
    	
        Thread.__init__(self)
        self.num = num
        result = channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def run(self):
        print(" [x] Enviando2")
        string = toserver.call("down"+self.num)
        print(string)
        #filename = tkFileDialog.asksaveasfilename(initialdir = "/",title = "",filetypes = (("all files","*.*")))
        if '@' in string :
        	filename, data = string.split('@', 1)
        	print("str: "+data)
        	data += "=" * ((4 - len(data) % 4) % 4)
        	arquivo = base64.b64decode(data)
	        with open("Client_peer/"+filename, 'wb') as f:
		        f.write(arquivo)
        

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        channel.basic_publish(exchange='',
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



url = os.environ.get('tkxllkea', 'amqp://popzhidh:Oqlcsw9vbHel4zMcZbTQv2z7sH0ZoNxG@spider.rmq.cloudamqp.com/popzhidh')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

b = Recieve()
toserver = Send(None)
topeer = SendPeer(None)
user=""
inicio = Tk()
Application(inicio)
inicio.mainloop()