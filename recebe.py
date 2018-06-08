#!/usr/bin/env
# -*- coding: utf-8 -*-
import pika
import subprocess
import base64
import time, os, timeit
from threading import Thread

class Recieve(Thread):

    def on_request(self, ch, method, props, body):

        filename = ''
        imgdata = ""
        response = ""

        if "down" in body:
            print(body)
            arq = open("Server_peer/.todownload.txt", "r")
            files = arq.readlines()
            arq.close()

            for f in files:
                oi,file = f.split("/",1)
                erro,send = body.split("down",1)
                print(file, "."+send)
                if "."+send == file:
                    stri = ""
                    arquivo,erro = file.split("\n",1)
                    with open("Server_peer/"+file, "rb") as imageFile:
                        stri = base64.b64encode(imageFile.read())
                    print("stri: "+stri)
                    response = ""
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

    def fib():
        
        str = None
        with open("/home/douglas/Documentos/Trabalho_sd/oi.txt", "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
        

        arq = open("str.txt", "r")
        string = arq.read()
        print(string)
        arq.close()
        return string

a = Recieve()
a.start()