class ExamplePlugin:
    def __init__(self, fast_stream):
        self.fast_stream = fast_stream

    async def startup(self):
        print("Plugin is starting up.")

    async def shutdown(self):
        print("Plugin is shutting down.")
