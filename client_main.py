import sys
from PyQt5 import QtWidgets
from chatbot.chat_gui import ChatGUI
from loguru import logger
from datetime import datetime

logger.add(f'main-{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}.log')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ChatGUI()
    sys.exit(app.exec_())
