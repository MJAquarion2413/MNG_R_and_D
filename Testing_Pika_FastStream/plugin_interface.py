from PySide6.QtCore import QObject, Signal

class PluginInterface(QObject):
    data_ready = Signal(str)

    def initialize(self, app_context):
        raise NotImplementedError

    def handle_message(self, message: str):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError
