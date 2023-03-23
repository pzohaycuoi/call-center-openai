import os
import logging
import json
from dotenv import load_dotenv

import common
from azurespeechservice import SoundFileToText
from chatbot import ChatApp


common.logger_config()
logger = logging.getLogger("file")


def audiofile_to_openai(file):
    """
    When there is an item created in the blob
    An event will be fired and trigger this Azure Functions
    1. Send the audio file to Azure Speech To Text for transcribe
    2. Transcribe send to OpenAI provide context
    3. Get the question and table list from json in root folder
    4. Ask each question without retaining the conversation
    5. For each question OpenAI's response will be insert into database

    Args:
        file (string): Path to the audio file, can be os system path or url to the content
    """
    speech_app = SoundFileToText()
    logger.info("Transcribing audio")
    transcribe = speech_app.transcribe(file)

    chat_app = ChatApp()
    logger.info("Sending transcribe to OpenAI")
    chat_app.chat(transcribe)

    question_file_path = common.convert_to_realpath("../tbl_col_question_list.json")
    tbl_info = json.loads(question_file_path)
    db_stored_proc = tbl_info["tables"][0]["storedprocedure"]
    col_question_list = tbl_info["tables"][0]["columns"]
    for col in col_question_list:
        