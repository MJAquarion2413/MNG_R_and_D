import pytest
import threading
from unittest.mock import MagicMock, patch
from sender import MessageSender
from receiver import MessageReceiver


@pytest.fixture
def mock_pika():
    with patch('pika.BlockingConnection') as mock:
        # Mocking to automatically call the callback when basic_consume is called
        def fake_consume(queue, on_message_callback, auto_ack):
            # Simulating callback being triggered by message consumption
            on_message_callback(None, None, None, b'Test message')

        mock.return_value.channel.return_value.queue_declare.return_value = MagicMock()
        mock.return_value.channel.return_value.basic_consume.side_effect = fake_consume
        yield mock


def send_messages(sender, messages):
    for message in messages:
        sender.send_message(message)


def test_concurrent_sending(mock_pika):
    sender = MessageSender()
    messages = ["Message 1", "Message 2", "Message 3"]
    threads = [threading.Thread(target=send_messages, args=(sender, messages)) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Check if messages are sent without any issue
    assert sender.channel.basic_publish.call_count == 15
    sender.close()


def receive_messages(receiver, callback, consume_times=1):
    for _ in range(consume_times):
        receiver.start_consuming(callback=callback)


def test_concurrent_receiving(mock_pika):
    receiver = MessageReceiver()
    callback = MagicMock()
    threads = [threading.Thread(target=receive_messages, args=(receiver, callback, 3)) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Assuming each thread starts the consuming process 3 times
    assert callback.call_count == 6
    receiver.stop_consuming()
