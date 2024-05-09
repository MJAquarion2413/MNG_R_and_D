from plugin_interface import PluginInterface
from faststream import FastStream


class ExamplePlugin(PluginInterface):
    def __init__(self, fast_stream: FastStream):
        super().__init__()
        self.fast_stream = fast_stream

    async def initialize(self, app_context):
        print("Plugin initialized with FastStream!")
        self.fast_stream.on_startup(self.setup)
        self.fast_stream.after_shutdown(self.teardown)

    async def setup(self):
        print("Plugin setup tasks...")

    async def teardown(self):
        print("Plugin cleanup tasks...")

    def handle_message(self, message: str):
        print(f"Received message in plugin: {message}")

    def cleanup(self):
        print("Cleaning up plugin resources...")
