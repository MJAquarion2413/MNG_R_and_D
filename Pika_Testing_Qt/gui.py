from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from message_handler import send_message


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.btn1 = QPushButton('Activate Widget 1', self)
        self.btn1.clicked.connect(lambda: send_message({"function": "activate_widget1"}))

        self.btn2 = QPushButton('Activate Widget 2', self)
        self.btn2.clicked.connect(lambda: send_message({"function": "activate_widget2"}))

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

    def show_popup(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Task Confirmation")
        msg.setText(message)
        msg.exec()

    def activate_widget1(self):
        self.show_popup("Widget 1 Activated")

    def activate_widget2(self):
        self.show_popup("Widget 2 Activated")


def run():
    app = QApplication([])
    ex = MyApp()
    ex.show()
    app.exec()
