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

        if body.find(".txt") > 0:

            file = body[::-1]
            body, rest = file.split('/', 1)
            print(body)
            file = body[::-1]

            arq = open("Server_peer/.recebidos.txt", "w")
            filename = 'Server_peer/.'+file  # I assume you have a way of picking unique filenames
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