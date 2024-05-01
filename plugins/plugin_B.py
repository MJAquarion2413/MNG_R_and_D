# plugins/PopupPlugin.py
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject
from signal_warehouse import SignalWarehouse

class Plugin(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        SignalWarehouse.connect_signal('buttonPressedSignal', self.show_popup)

    def show_popup(self):
        message_box = QMessageBox()
        message_box.setText("Signal received, task completed")
        message_box.buttonClicked.connect(self.emit_back_signal)
        message_box.exec_()

    def emit_back_signal(self):
        SignalWarehouse.emit_signal('taskCompletedSignal')

    def enable(self):
        print("PopupPlugin enabled")

    def disable(self):
        print("PopupPlugin disabled")
