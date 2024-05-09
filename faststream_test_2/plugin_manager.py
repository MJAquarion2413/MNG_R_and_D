class PluginManager:
    def __init__(self, fast_stream):
        self.plugins = []
        self.fast_stream = fast_stream

    def load_plugins(self):
        # Example: Load an instance of ExamplePlugin
        plugin = ExamplePlugin(self.fast_stream)
        self.plugins.append(plugin)
        self.fast_stream.on_startup(plugin.startup)
        self.fast_stream.on_shutdown(plugin.shutdown)
