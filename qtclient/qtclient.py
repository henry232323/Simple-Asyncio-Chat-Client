from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QTextCursor
from PyQt5.QtCore import Qt
from quamash import QEventLoop

import asyncio, sys, argparse
from asyncio import async as aioasync
from client import Client

class Gui(QWidget):
    def __init__(self, loop, client, parent=None, **kwargs):
        super(__class__, self).__init__(**kwargs)
        self.client = client
        self.client.output = self.output
        self.loop = loop
        self.resize(400, 300)
        self.setWindowTitle('Garbage Chat')
        self.setWindowIcon(QIcon('xMpZUxES.jpg'))
        self.maxlines = 15
        self.initialize()
        self.show()

    def send(self, *obj):
        self.client.send(self.userInput.text())
        self.userInput.setText("")

    def output(self, data):
        self.outTE.insertPlainText(data)
        self.set_text_cursor_pos(-1)
            
    def initialize(self):
        while not self.client.user:
            text, ok = QInputDialog.getText(self, 'Handle', 
                'Enter your handle:')
            self.client.user = text
        
        userlabel = QLabel(self.client.user, self)
        userlabel.move(5,5)
        userlabel.setStyleSheet("color:#444444; font-size: 15px;")
        
        self.outTE = QTextEdit("", self)
        self.outTE.setReadOnly(True)
        self.outTE.setMouseTracking(True)
        self.outTE.resize(362,200)
        self.outTE.textSelected = False
        self.outTE.move(25,37)

        sendButton = QPushButton("Send")
        sendButton.clicked.connect(self.send)

        userInput = QLineEdit(self)
        userInput.setStyleSheet("background: white; width:300px; border:2px solid #444444; font-size: 13px;")
        self.userInput = userInput
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(userInput)
        hbox.addWidget(sendButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            self.send()

    def get_text_cursor(self):
        return self.outTE.textCursor()

    def set_text_cursor_pos(self, value):
        tc = self.get_text_cursor()
        tc.setPosition(value, QTextCursor.KeepAnchor)
        self.outTE.setTextCursor(tc)

    def get_text_cursor_pos(self):
        return self.get_text_cursor().position()
            
class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        loop = QEventLoop(self)
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        self.userClient = Client(self.loop, args["user"])

        self.loop.create_task(self.start())

        self.gui = Gui(self.loop, self.userClient)
        loop.run_forever()
        
    async def start(self):
        coro = self.loop.create_connection(lambda: self.userClient, args["addr"], args["port"])
        aioasync(coro)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client settings")
    parser.add_argument("--user", type=str)
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    args = vars(parser.parse_args())

    App()
