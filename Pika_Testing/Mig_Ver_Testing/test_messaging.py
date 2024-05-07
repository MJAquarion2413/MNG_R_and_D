import pytest
from unittest.mock import MagicMock, patch
from sender import MessageSender
from receiver import MessageReceiver


@pytest.fixture
def mock_pika():
    with patch('pika.BlockingConnection') as mock:
        # Set up mock to automatically call the callback when consuming messages
        def fake_consume(queue, on_message_callback, auto_ack):
            # Simulate a message being received
            on_message_callback(None, None, None, b'Test message')

        mock.return_value.channel.return_value.queue_declare.return_value = MagicMock()
        mock.return_value.channel.return_value.basic_consume.side_effect = fake_consume
        yield mock


def test_send_message(mock_pika):
    sender = MessageSender()
    sender.send_message("Test message")
    assert sender.channel.basic_publish.called
    sender.close()


def test_receive_message(mock_pika):
    receiver = MessageReceiver()
    callback = MagicMock()
    receiver.start_consuming(callback=callback)
    callback.assert_called_once_with(None, None, None, b'Test message')
    receiver.stop_consuming()

# More tests can be added for various scenarios and message contents
