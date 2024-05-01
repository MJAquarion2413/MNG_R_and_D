# plugins/ButtonPlugin.py
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import QObject, Signal


class Plugin(QObject):
    buttonPressedSignal = Signal()

    def __init__(self, main_window, signal_warehouse):
        super().__init__(main_window)
        self.main_window = main_window
        self.signal_warehouse = signal_warehouse
        self.signal_warehouse.register_signal('buttonPressedSignal', self.buttonPressedSignal)
        self.setup_ui()

    def setup_ui(self):
        self.button = QPushButton("Press Me")
        self.button.clicked.connect(self.emit_signal_to_popup)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        widget = QWidget()
        widget.setLayout(layout)
        self.main_window.setCentralWidget(widget)

    def emit_signal_to_popup(self):
        self.signal_warehouse.emit_signal('buttonPressedSignal')

    def enable(self):
        print("ButtonPlugin enabled")

    def disable(self):
        print("ButtonPlugin disabled")