import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QThread, Signal
from aio_pika import connect, Message


class AioPikaThread(QThread):
    message_received = Signal(str)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.aio_pika_task())

    async def aio_pika_task(self):
        # Setup connection, ensure RabbitMQ is running and accessible
        connection = await connect("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        queue = await channel.declare_queue("gui_queue", auto_delete=True)

        async for message in queue:
            async with message.process():
                self.message_received.emit(message.body.decode())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Waiting for messages...", self)
        self.setCentralWidget(self.label)
        self.resize(400, 300)

        # Start the background thread
        self.aio_pika_thread = AioPikaThread()
        self.aio_pika_thread.message_received.connect(self.update_label)
        self.aio_pika_thread.start()

    def update_label(self, text):
        self.label.setText(text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
