# test_app.py

import sys
import pytest
from PySide6.QtWidgets import QApplication
from aio_pika import connect_robust
from asyncio import get_event_loop

# Assume you have a QMainWindow or similar top-level widget
from main_window import MainWindow


@pytest.fixture
def qt_app(qtbot):
    """Fixture to initialize Qt application."""
    app = QApplication.instance()  # Checks if an instance already exists
    if not app:  # If no instance, create a new one
        app = QApplication(sys.argv)
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    yield app, main_window
    # Proper cleanup: Close the main window and quit the application
    main_window.close()
    app.quit()


@pytest.fixture
async def aio_pika_connection():
    """Fixture to initialize AIO Pika connection."""
    # Update the connection string to your RabbitMQ server
    connection = await connect_robust("amqp://guest:guest@localhost/")
    yield connection
    await connection.close()


@pytest.mark.asyncio
async def test_aio_pika_connection(aio_pika_connection):
    """Test the AIO Pika connection."""
    assert aio_pika_connection.is_closed is False


def test_main_window(qt_app):
    """Test the main window load."""
    app, main_window = qt_app
    assert main_window.isVisible()

# Add more tests as needed
