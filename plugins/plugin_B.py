# plugins/PopupPlugin.py
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject

class Plugin(QObject):
    def __init__(self, main_window, signal_warehouse):
        super().__init__(main_window)
        self.signal_warehouse = signal_warehouse
        self.signal_warehouse.connect_signal('buttonPressedSignal', self.show_popup)

    def show_popup(self):
        message_box = QMessageBox()
        message_box.setText("Signal received, task completed")
        message_box.exec_()  # Block until closed

    def enable(self):
        print("PopupPlugin enabled")

    def disable(self):
        print("PopupPlugin disabled")