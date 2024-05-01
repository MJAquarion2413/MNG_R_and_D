from PySide6.QtCore import QObject, Signal


class SignalWarehouse(QObject):
    def __init__(self):
        super().__init__()
        self.signals = {}  # Dictionary to store dynamic signals

    def register_signal(self, signal_name, signal):
        """Register a new signal."""
        self.signals[signal_name] = signal

    def get_signal(self, signal_name):
        """Retrieve a registered signal."""
        if signal_name in self.signals:
            return self.signals[signal_name]
        else:
            raise ValueError(f"No signal found with the name: {signal_name}")

    def connect_signal(self, signal_name, slot):
        """Connect a registered signal to a slot/function."""
        signal = self.get_signal(signal_name)
        signal.connect(slot)

    def disconnect_signal(self, signal_name, slot):
        """Disconnect a registered signal from a slot/function."""
        signal = self.get_signal(signal_name)
        signal.disconnect(slot)

    def emit_signal(self, signal_name, *args):
        """Emit a registered signal with the given arguments."""
        signal = self.get_signal(signal_name)
        signal.emit(*args)