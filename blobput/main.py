import os
import logging
from dotenv import load_dotenv

import common
from azurespeechservice import SoundFileToText
from chatbot import ChatApp


common.logger_config()
logger = logging.getLogger("file")


def audiofile_to_openai(file):
    speech_app = SoundFileToText()
    trans_text = speech_app.convert_to_text(file)
    chat_app = ChatApp()
    response_text = chat_app.chat(trans_text)
    