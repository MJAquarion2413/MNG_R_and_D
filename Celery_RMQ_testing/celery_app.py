from celery import Celery

# Make sure to have RabbitMQ running on localhost, simply have erlang and
# rabbitmq installed and type in search bar and server start should pop up
app = Celery('my_app',
             broker='amqp://localhost',  # RabbitMQ as broker
             backend='rpc://')


@app.task
def first_task(arg):
    return f"Processed {arg}"


@app.task
def create_snake():
    return "Snake created"
