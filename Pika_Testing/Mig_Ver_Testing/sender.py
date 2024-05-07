import pika

class MessageSender:
    def __init__(self, queue_name='hello', host='localhost'):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=message)
        print(f" [x] Sent '{message}'")

    def close(self):
        self.connection.close()
