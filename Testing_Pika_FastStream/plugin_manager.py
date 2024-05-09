from faststream import FastStream
from example_plugin import ExamplePlugin


class PluginManager:
    def __init__(self, fast_stream: FastStream):
        self.plugins = []
        self.fast_stream = fast_stream

    def load_plugins(self):
        self.plugins.append(ExamplePlugin(self.fast_stream))

    async def initialize(self):
        for plugin in self.plugins:
            await plugin.initialize(self.fast_stream)

    def close(self):
        for plugin in self.plugins:
            plugin.cleanup()
