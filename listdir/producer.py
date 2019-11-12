import pika
import json


def send_messages(messages):
    channel, connection = connect_to_broker('localhost')
    channel.queue_declare(queue='listdir')
    for message in messages:
        channel.basic_publish(exchange='', routing_key='listdir', body=json.dumps(message, indent=4))
    connection.close()


def connect_to_broker(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    return channel, connection
