import asyncio

import pika
import json


def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Ensure 'durable' matches the initial declaration. Set to True or False as needed.
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='task_queue', body=json.dumps(message))
    connection.close()


async def async_callback(channel, method, properties, body, callback):
    await callback(json.loads(body))


def start_consumer(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    # Wrap the async_callback with the appropriate coroutine handling.
    on_message_callback = lambda ch, method, properties, body: asyncio.run(
        async_callback(ch, method, properties, body, callback))

    channel.basic_consume(queue='task_queue', on_message_callback=on_message_callback, auto_ack=True)
    print('Waiting for messages...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
