# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from houndify_api.houndify import TextHoundClient, StreamingHoundClient
from houndify_api.settings import CLIENT_KEY, CLIENT_ID, USER, REQUEST_INFO, FORMAT, CHANNELS, RATE, CHUNK, BUFFER_SIZE
from houndify_api.speech_listener import SpeechListener
from mercedes_api.mercedes_cv_api import MercedesCvApi as MercedesApi
from mercedes_api.settings import AUTH_TOKEN, VEHICLE_ID
from mercedes_api.mercedes_response_handler import MercedesResponseHandler
import pyaudio
from chatbot.settings import ROLE_DESIGN_MAPPING
import traceback
from loguru import logger
import os


class ChatGUI(QtWidgets.QMainWindow):
    """
    This class is responsible for the Graphical User Interface
    of the mercedes chatbot.
    It handles written requests when the user presses Enter
    and it handles voice requests when the user presses on the button
    with the microphone symbol.
    """
    __instance = None
    __initialized = False

    def __new__(cls):
        if not ChatGUI.__instance:
            ChatGUI.__instance = QtWidgets.QMainWindow.__new__(cls)
        return ChatGUI.__instance

    def __init__(self):
        if not self.__initialized:
            super(ChatGUI, self).__init__()

            # load the static gui
            # and define the layout size
            self.ui = uic.loadUi('qt5chatgui.ui', self)
            self.scroll_area = self.findChild(QtWidgets.QScrollArea, 'scroll_area')
            self.scroll_area_widget_contents = self.findChild(QtWidgets.QWidget, 'scroll_area_widget_contents')
            self.layout = self.scroll_area_widget_contents.layout()
            self.layout.setColumnStretch(0, 4)
            self.layout.setColumnStretch(4, 8)

            # text input and speech button connected with their event handlers
            self.text_input = self.findChild(QtWidgets.QLineEdit, 'text_input')
            self.text_input.returnPressed.connect(self.on_enter)
            self.speech_button = self.findChild(QtWidgets.QPushButton, 'speech_button')
            self.speech_button.pressed.connect(self.on_speech)

            # create initial chat bubble with a greeting
            # gets overridden after every request
            greeting = 'How can I help you?'
            self.last_chat_bubble = QtWidgets.QLabel(greeting)
            self.last_chat_bubble.setFont(QtGui.QFont('Ubuntu', 16))
            self.last_chat_bubble.setAlignment(QtCore.Qt.AlignCenter)
            self.last_chat_bubble.setStyleSheet(ROLE_DESIGN_MAPPING['bot'])
            self.last_chat_bubble.setFixedSize(self._label_size(greeting), 51)
            self.layout.addWidget(self.last_chat_bubble, 0, 0)
            self.show()

            # connections to houndify and mercedes apis
            self.houndify_client = TextHoundClient(CLIENT_ID, CLIENT_KEY, USER, REQUEST_INFO)
            self.mercedes = MercedesApi(AUTH_TOKEN)

            self.__initialized = True

    def handle_houndify_response(self, res):
        """
        Handles the response json from Houndify.
        First gives the general response from houndify to the user.
        Secondly, if the request is a Mercedes connected vehicle usecase,
        retrieves and shows a more specific answer to the request.
        :param res: response json
        :return:
        """
        try:
            user_result = res['AllResults'][0]['WrittenResponseLong']
            self.last_chat_bubble = self.add_chat_bubble(text=user_result,
                                                         last_bubble=self.last_chat_bubble,
                                                         role='bot')
        except KeyError:
            logger.warning(str(res))
            try:
                if res['Error'] == b'Over daily limit\n':
                    self.last_chat_bubble = self.add_chat_bubble(text='Over daily limit at Houndify :(',
                                                                 last_bubble=self.last_chat_bubble,
                                                                 role='bot')
            except:
                logger.warning(traceback.format_exc())

        try:
            intent = res['AllResults'][0]['Result']
            if 'car' in intent.keys():
                res, vehicle_part, user_result = MercedesResponseHandler.on_mercedes_indent(intent['car'],
                                                                                            self.mercedes, VEHICLE_ID)
                if user_result:
                    self.add_chat_bubble_big_text(text=user_result)
                elif res:
                    user_result = MercedesResponseHandler.json_information_response_readable(res, vehicle_part)
                    self.add_chat_bubble_big_text(text=user_result)
        except KeyError:
            logger.warning(traceback.format_exc())

    @QtCore.pyqtSlot()
    def on_enter(self):
        """
        The slot / event handler if the user presses Enter within the text box.
        Gets the user input (text) and passes it to Houndify.
        :return:
        """
        request = self.text_input.text()
        self.text_input.clear()
        self.last_chat_bubble = self.add_chat_bubble(text=request,
                                                     last_bubble=self.last_chat_bubble,
                                                     role='user')
        # request to Houndify
        res = self.houndify_client.query(request)
        self.handle_houndify_response(res)

    @QtCore.pyqtSlot()
    def on_speech(self):
        """
        The slot / event handler if the user presses on the speech button
        Streams the user input (audio) to Houndify.
        :return:
        """
        speech_client = StreamingHoundClient(CLIENT_ID, CLIENT_KEY, USER, REQUEST_INFO)
        speech_client.start(SpeechListener())

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)

        while True:
            samples = stream.read(BUFFER_SIZE)
            if len(samples) == 0:
                break
            if speech_client.fill(samples):
                break

        stream.stop_stream()
        stream.close()
        p.terminate()
        res = speech_client.finish()
        user_utterance = 'Sorry, your request was not recognized.'
        try:
            user_utterance = res['Disambiguation']['ChoiceData'][0]['Transcription']
        except KeyError:
            pass
        self.last_chat_bubble = self.add_chat_bubble(user_utterance, self.last_chat_bubble, role='user')
        self.handle_houndify_response(res)

    def add_chat_bubble(self, text, last_bubble, role='bot'):
        """
        Helper method for adding chat bubbles to the chat interface.
        Uses information about the last added chat bubble (like size, position, design)
        in order to create the new chat bubble.
        Different styles for user and bot chat bubbles.
        :param text: the chat bubbles content
        :param last_bubble: the previously added chat bubble
        :param role: bot OR user
        :return: returns the newly created chat bubble
        """
        # information from the previous chat bubble
        last_rect = last_bubble.geometry()
        height = last_rect.height()

        # create the new chat bubble (label)
        label = QtWidgets.QLabel(text)
        label.setFont(last_bubble.font())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(ROLE_DESIGN_MAPPING[role])
        label.setFixedSize(self._label_size(text), height)

        # positioning based on the role
        new_x = 0
        if role == 'user':
            new_x = 8
        new_y = self.layout.indexOf(last_bubble) + 1

        # add the label to the layout and scroll down
        self.layout.addWidget(label, new_y, new_x)
        label.show()
        self.scroll_area.ensureWidgetVisible(label)

        return label

    def add_chat_bubble_big_text(self, text):
        """
        Helper method specifically for the self defined Mercedes responses.
        Some of the answers span over multiple lines, which is turned into
        multiple short responses instead of a single big one.
        :param text: the Mercedes response (already humand readable)
        :return:
        """
        if os.linesep in text:
            lines = text.split(os.linesep)
            for line in lines:
                self.last_chat_bubble = self.add_chat_bubble(line, self.last_chat_bubble, role='bot')
        else:
            self.last_chat_bubble = self.add_chat_bubble(text, self.last_chat_bubble, role='bot')

    def _label_size(self, text):
        """
        Defines chat bubble (label) size based on the amount of text in it.
        :param text: the labels future text
        :return: returns the labels target size
        """
        text_length = len(text)
        if text_length < 5:
            return text_length * 25
        elif 5 <= text_length < 10:
            return text_length * 20
        elif 10 < text_length < 30:
            return text_length * 11
        else:
            return text_length * 11
