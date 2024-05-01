from PySide6.QtCore import QObject, Signal


class SignalWarehouse(QObject):
    # PlaceHolder signals
    dataUpdated = Signal(str)
    taskCompleted = Signal()

    def __init__(self):
        super().__init__()

    @classmethod
    def get_signal(cls, signal_name):
        """Retrieve a signal by its name."""
        if hasattr(cls, signal_name):
            return getattr(cls, signal_name)
        else:
            raise ValueError(f"No signal found with the name: {signal_name}")

    @classmethod
    def connect_signal(cls, signal_name, slot):
        """Connect a signal to a slot/function."""
        signal = cls.get_signal(signal_name)
        signal.connect(slot)

    @classmethod
    def disconnect_signal(cls, signal_name, slot):
        """Disconnect a signal from a slot/function."""
        signal = cls.get_signal(signal_name)
        signal.disconnect(slot)

    @classmethod
    def emit_signal(cls, signal_name, *args):
        """Emit a signal with the given arguments."""
        signal = cls.get_signal(signal_name)
        signal.emit(*args)
