# plugins/ButtonPlugin.py
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import QObject
from signal_warehouse import SignalWarehouse


class Plugin(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setup_ui()
        SignalWarehouse.connect_signal('taskCompletedSignal', self.complete_chain)

    def setup_ui(self):
        self.button = QPushButton("Press Me")
        self.button.clicked.connect(self.emit_signal_to_popup)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        widget = QWidget()
        widget.setLayout(layout)
        self.main_window.setCentralWidget(widget)

    def emit_signal_to_popup(self):
        SignalWarehouse.emit_signal('buttonPressedSignal')

    def complete_chain(self):
        QMessageBox.information(None, "Notification", "Signal chain completed")

    def enable(self):
        print("ButtonPlugin enabled")

    def disable(self):
        print("ButtonPlugin disabled")
