#!# -*- coding; utf-8 -*-
import pika
import subprocess
import base64
import time, os, timeit

url = os.environ.get('tkxllkea', 'amqp://popzhidh:Oqlcsw9vbHel4zMcZbTQv2z7sH0ZoNxG@spider.rmq.cloudamqp.com/popzhidh')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='rpc_queue')
    
def on_request(ch, method, props, body):
    arq = open('cadastro.txt','r')
    string = arq.readlines()
    arq.close()

    a=0
    b=0
    cont = 0
    for s in range(len(string)-1):
        cont = cont+1
        #print(string[s]+string[s+1],body)
        if body+'\n'==string[s]+string[s+1]:
            response = str(cont)+"acerto mizeravi"    
            a=100
            b=100
            break
        elif body+'\n'=="cad."+string[s]+string[s+1]:
            print("uh")
            response = str(cont)+"acerto mizeravi"
            b=100
            a=100
            break
        s = s+1
    if a == 0:
        response = "erro mizeravi"
    if b == 0 and "cad." in body:
        errado, certo = body.split("cad.")
        arq = open('cadastro.txt','a')
        arq.write(str(certo)+"\n")
        arq.close()
        response = "erro mizeravi"

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()