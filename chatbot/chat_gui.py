# This Python file uses the following encoding: utf-8
import sys
from functools import partial
from PyQt5 import QtWidgets, uic, QtCore
from houndify_api.houndify import TextHoundClient
from houndify_api.settings import CLIENT_KEY, CLIENT_ID, USER, REQUEST_INFO
from mercedes_api.mercedes_cv_api import MercedesCvApi as MercedesApi
from mercedes_api.settings import AUTH_TOKEN, VEHICLE_ID
from mercedes_api.mercedes_response_handler import MercedesResponseHandler
from chatbot.settings import ROLE_DESIGN_MAPPING
import traceback
from loguru import logger


class ChatGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(ChatGUI, self).__init__()
        self.ui = uic.loadUi('qt5chatgui.ui', self)
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, 'scroll_area')
        # self.vertical_bar = self.scroll_area.verticalScrollBar()
        self.scroll_area_widget_contents = self.findChild(QtWidgets.QWidget, 'scroll_area_widget_contents')
        self.layout = self.scroll_area_widget_contents.layout()
        # self.layout.setColumnStretch(0, 2)
        # self.layout.setColumnStretch(2, 4)

        self.text_input = self.findChild(QtWidgets.QLineEdit, 'text_input')
        self.text_input.returnPressed.connect(self.on_enter)

        # gets overridden after every request
        self.last_chat_bubble = self.findChild(QtWidgets.QLabel, 'label_greet')
        self.show()

        self.houndify_client = TextHoundClient(CLIENT_ID, CLIENT_KEY, USER, REQUEST_INFO)
        self.mercedes = MercedesApi(AUTH_TOKEN)

    @QtCore.pyqtSlot()
    def on_enter(self):
        request = self.text_input.text()
        self.text_input.clear()
        self.last_chat_bubble = self.add_chat_bubble(text=request,
                                                     last_bubble=self.last_chat_bubble,
                                                     role='user')
        # request to Houndify
        res = self.houndify_client.query(request)
        user_result = res['AllResults'][0]['WrittenResponseLong']
        self.last_chat_bubble = self.add_chat_bubble(text=user_result,
                                                     last_bubble=self.last_chat_bubble,
                                                     role='bot')

        try:
            intent = res['AllResults'][0]['Result']
            if 'car' in intent.keys():
                res, vehicle_part, user_result = MercedesResponseHandler.on_mercedes_indent(intent['car'], self.mercedes, VEHICLE_ID)
                if user_result:
                    self.add_chat_bubble_big_text(text=user_result)
                elif res:
                    user_result = MercedesResponseHandler.json_information_response_readable(res, vehicle_part)
                    self.add_chat_bubble_big_text(text=user_result)
        except KeyError:
            logger.warning(traceback.format_exc())

    def add_chat_bubble(self, text, last_bubble, role='bot'):
        last_rect = last_bubble.geometry()
        x = last_rect.x()
        y = last_rect.y()
        width = last_rect.width()
        height = last_rect.height()

        label = QtWidgets.QLabel(text)
        label.setFont(last_bubble.font())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(ROLE_DESIGN_MAPPING[role])
        label.setFixedSize(self._label_size(text), height)

        new_x = 0
        if role == 'user':
            new_x = 1
        new_y = self.layout.indexOf(last_bubble) + 1

        self.layout.addWidget(label, new_y, new_x)
        label.show()

        self.scroll_area.ensureWidgetVisible(label)
        #QtCore.QTimer.singleShot(0, partial(self.scroll_area.ensureWidgetVisible, label))
        return label

    def add_chat_bubble_big_text(self, text):
        # TODO: do I need os independent linebreaks?
        if '\n' in text:
            lines = text.split('\n')
            for line in lines:
                self.last_chat_bubble = self.add_chat_bubble(line, self.last_chat_bubble, role='bot')
        else:
            self.last_chat_bubble = self.add_chat_bubble(text, self.last_chat_bubble, role='bot')

    def _label_size(self, text):
        text_length = len(text)
        if text_length < 5:
            return text_length * 25
        elif 5 <= text_length < 10:
            return text_length * 20
        elif 10 < text_length < 30:
            return text_length * 11
        else:
            return text_length * 11
