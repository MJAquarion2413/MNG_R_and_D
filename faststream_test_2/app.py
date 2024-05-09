import sys
from PySide6.QtWidgets import QApplication
from faststream import FastStream
from plugin_manager import PluginManager

fast_stream = FastStream()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Setup FastStream lifecycle hooks
    @fast_stream.on_startup
    async def start_services():
        print("Starting services...")

    @fast_stream.after_startup
    async def post_start():
        print("Services started.")

    @fast_stream.on_shutdown
    async def shutdown_services():
        print("Shutting down services...")

    @fast_stream.after_shutdown
    async def post_shutdown():
        print("Services shut down.")

    # Initialize PluginManager with FastStream
    manager = PluginManager(fast_stream)
    manager.load_plugins()

    # Running FastStream and Qt Event Loop
    fast_stream.run_in_thread()  # Assuming you modify FastStream to support running in a separate thread

    sys.exit(app.exec())
