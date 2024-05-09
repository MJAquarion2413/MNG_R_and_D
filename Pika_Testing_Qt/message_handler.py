import pika
import json

def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')
    channel.basic_publish(exchange='', routing_key='task_queue', body=json.dumps(message))
    connection.close()

def start_consumer(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')

    channel.basic_consume(queue='task_queue', on_message_callback=lambda ch, method, properties, body: callback(json.loads(body)), auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()
