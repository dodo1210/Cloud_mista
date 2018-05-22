#!# -*- coding; utf-8 -*-
import pika, os
import subprocess
import Image
import base64


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('nfwwsnsc', 'amqp://nfwwsnsc:6q16k6MT2TnoQdnNq2FZwdbLJNPb2dNU@crocodile.rmq.cloudamqp.com/nfwwsnsc')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='rpc_queue')

def fib(n):
    return n

def on_request(ch, method, props, body):
    string = body
    ant = None
    
   
    print(body)
    ah = base64.b64decode(body)
    filename = 'vai.txt'  # I assume you have a way of picking unique filenames

   # with open(filename, 'wb') as f:
        f.write(ah)
    ant = body

    py_arq = "niveis_de_cinza.py"

    processo = subprocess.call(["python "+py_arq], shell=True)
    response = fib(string)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=10)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()