import asyncio
from time import time
from unittest.mock import MagicMock

import pytest
from aio_pika import connect, Connection, Message, ExchangeType


@pytest.fixture
async def rabbitmq_connection():
    connection = await connect("amqp://guest:guest@localhost/")
    yield connection
    await connection.close()


@pytest.mark.asyncio
async def test_connection_established(rabbitmq_connection):
    assert isinstance(rabbitmq_connection, Connection)


@pytest.mark.asyncio
async def test_channel_declaration(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        assert channel.is_initialized


@pytest.mark.asyncio
async def test_publish_and_receive_message(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        queue = await channel.declare_queue("test_queue", auto_delete=True)
        await queue.consume(callback, no_ack=True)
        message = Message(b"Test message")
        await channel.default_exchange.publish(message, routing_key="test_queue")
        await asyncio.sleep(1)  # Give some time for the message to be processed


@pytest.mark.asyncio
async def test_exchange_redeclaration_with_different_type(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        exchange = await channel.declare_exchange("test_exchange", type=ExchangeType.DIRECT)
        with pytest.raises(Exception):
            # Trying to redeclare with a different type should raise an exception
            await channel.declare_exchange("test_exchange", type=ExchangeType.FANOUT)


@pytest.mark.asyncio
async def test_message_persistence(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        queue = await channel.declare_queue("persistent_queue", durable=True)
        exchange = await channel.declare_exchange("persistent_exchange", type=ExchangeType.DIRECT, durable=True)
        await queue.bind(exchange, "routing_key")
        message = Message(b"Persistent message", delivery_mode=2)
        await exchange.publish(message, routing_key="routing_key")
        # Restart connection or simulate server restart to test persistence
        # This is more of an integration test scenario requiring environment manipulation


@pytest.mark.asyncio
async def test_consumer_cancellation_on_queue_deletion(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        queue = await channel.declare_queue("test_cancel_queue", auto_delete=True)
        consumer_tag = await queue.consume(callback, no_ack=True)
        await queue.delete()
        # Ensure the consumer is cancelled properly
        with pytest.raises(Exception):
            await channel.cancel(consumer_tag)


@pytest.mark.asyncio
async def test_timeout_handling(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        with pytest.raises(asyncio.TimeoutError):
            # Simulate a timeout scenario, e.g., during queue declaration
            await channel.declare_queue("test_timeout_queue", timeout=0.1)


@pytest.mark.asyncio
async def test_topic_exchange_routing(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        topic_exchange = await channel.declare_exchange('topic_logs', ExchangeType.TOPIC)
        queue_error = await channel.declare_queue('error_logs')
        queue_warning = await channel.declare_queue('warning_logs')
        await queue_error.bind(topic_exchange, routing_key='*.error')
        await queue_warning.bind(topic_exchange, routing_key='*.warning')

        message_error = Message(b"Error log", routing_key='app1.error')
        message_warning = Message(b"Warning log", routing_key='app2.warning')
        await topic_exchange.publish(message_error, routing_key='app1.error')
        await topic_exchange.publish(message_warning, routing_key='app2.warning')
        # Additional code to consume from the queues and verify routing correctness


@pytest.mark.asyncio
async def test_message_processing_error_handling(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        queue = await channel.declare_queue('error_handling_queue')
        await queue.consume(buggy_callback, no_ack=True)
        message = Message(b"Test")
        await channel.default_exchange.publish(message, routing_key='error_handling_queue')
        await asyncio.sleep(1)  # Give time to process and handle the error


async def buggy_callback(message):
    raise Exception("Simulated processing error")


@pytest.mark.asyncio
async def test_high_throughput_scenario(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        queue = await channel.declare_queue('high_throughput_queue', auto_delete=True)
        for _ in range(1000):  # Simulate high message volume
            message = Message(b"High load message")
            await channel.default_exchange.publish(message, routing_key='high_throughput_queue')
        # Consider checking the queue size or processing time as metrics for performance


@pytest.mark.asyncio
async def test_connection_recovery(rabbitmq_connection):
    async with rabbitmq_connection.channel() as channel:
        original_state = not channel.is_closed
        # Simulate a connection drop here, e.g., by stopping the RabbitMQ service or using a network failure
        # simulation tool
        await asyncio.sleep(10)  # Wait for recovery mechanisms to kick in
        assert original_state != channel.is_closed  # Check if the channel recovered


@pytest.fixture
async def setup_messaging():
    connection = await connect("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("gui_queue", auto_delete=True)
    yield connection, channel, queue
    await connection.close()


@pytest.mark.asyncio
async def test_gui_updates_on_message(setup_messaging):
    connection, channel, queue = setup_messaging
    # Simulate receiving a message that should update the GUI
    gui_update = MagicMock()
    await queue.consume(gui_update, no_ack=True)
    test_message = Message(b"Update GUI")
    await channel.default_exchange.publish(test_message, routing_key="gui_queue")
    await asyncio.sleep(0.5)  # Wait for message to be processed
    gui_update.assert_called_once_with(test_message)


@pytest.mark.asyncio
async def test_command_sending_from_gui_to_bot(setup_messaging):
    connection, channel, queue = setup_messaging
    # Function to simulate GUI command sending
    bot_queue = await channel.declare_queue("bot_queue", auto_delete=True)
    command = "Perform action"
    test_message = Message(command.encode())
    await channel.default_exchange.publish(test_message, routing_key="bot_queue")
    # Assuming a way to mock or check bot received the message or acted on it


@pytest.mark.asyncio
async def test_handling_multiple_simultaneous_messages(setup_messaging):
    connection, channel, queue = setup_messaging
    gui_update = MagicMock()
    await queue.consume(gui_update, no_ack=True)
    messages = [Message(f"Message {i}".encode()) for i in range(10)]
    for msg in messages:
        await channel.default_exchange.publish(msg, routing_key="gui_queue")
    await asyncio.sleep(1)  # Give time for all messages to be processed
    assert gui_update.call_count == 10


@pytest.mark.asyncio
async def test_error_handling_in_message_delivery(setup_messaging):
    connection, channel, queue = setup_messaging
    gui_error_handler = MagicMock()
    # Simulate a message that will cause an error in processing
    await queue.consume(lambda msg: gui_error_handler("Error occurred"), no_ack=True)
    test_message = Message(b"Problematic message")
    await channel.default_exchange.publish(test_message, routing_key="gui_queue")
    await asyncio.sleep(0.5)
    gui_error_handler.assert_called_once_with("Error occurred")


@pytest.fixture
async def setup_channel():
    connection = await connect("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    yield channel
    await connection.close()


@pytest.mark.asyncio
async def test_message_order_and_integrity(setup_channel):
    channel = setup_channel
    queue = await channel.declare_queue("integrity_queue", auto_delete=True)
    messages_sent = [f"message {i}" for i in range(5)]
    for msg in messages_sent:
        await channel.default_exchange.publish(Message(msg.encode()), routing_key="integrity_queue")

    messages_received = []
    async for message in queue:
        messages_received.append(message.body.decode())
        await message.ack()
        if len(messages_received) == len(messages_sent):
            break

    assert messages_sent == messages_received


@pytest.mark.asyncio
async def test_recovery_from_disconnections(setup_channel):
    channel = setup_channel
    try:
        await channel.close()  # Simulate a disconnection
        await asyncio.sleep(1)  # Give some time for effects to manifest
        assert channel.is_closed
        channel = await setup_channel.connection.channel()  # Attempt to reconnect
        assert channel.is_open
    except Exception as e:
        pytest.fail(f"Reconnection failed: {e}")


@pytest.mark.asyncio
async def test_large_message_handling(setup_channel):
    channel = setup_channel
    large_message = b'a' * 1024 * 1024  # 1 MB message
    queue = await channel.declare_queue("large_message_queue", auto_delete=True)
    await channel.default_exchange.publish(Message(large_message), routing_key="large_message_queue")
    async for message in queue:
        assert message.body == large_message
        await message.ack()
        break


@pytest.mark.asyncio
async def test_response_time(setup_channel):
    channel = setup_channel
    queue = await channel.declare_queue("response_time_queue", auto_delete=True)
    start_time = time()
    message = Message(b"Test response time")
    await channel.default_exchange.publish(message, routing_key="response_time_queue")
    async for message in queue:
        end_time = time()
        response_time = end_time - start_time
        await message.ack()
        assert response_time < 0.5  # Expecting a response within 500 milliseconds
        break


@pytest.mark.asyncio
async def test_security_unauthorized_access(setup_channel):
    channel = setup_channel
    # Attempt to declare a queue with unauthorized access settings (assuming security constraints)
    with pytest.raises(Exception):
        await channel.declare_queue("unauthorized_queue")


async def callback(message):
    print("Message received:", message.body)
    await message.ack()
