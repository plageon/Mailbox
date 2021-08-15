import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from ReceiveWidget import ReceiveWidget
from SendWidget import SendWidget

class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("MailBox")
        self.send_widget = SendWidget()
        self.receive_widget = ReceiveWidget()

        self.send_button = QPushButton('Send an E-mail!', self)
        self.send_button.resize(200, 100)
        self.send_button.move(100, 200)

        self.receive_button = QPushButton('Check E-mails from your Mailbox!', self)
        self.receive_button.resize(200, 100)
        self.receive_button.move(500, 200)

        self.send_button.clicked.connect(self.open_send)
        self.receive_button.clicked.connect(self.open_receive)

    def open_send(self):
        self.send_widget.show()

    def open_receive(self):
        self.receive_widget.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())
