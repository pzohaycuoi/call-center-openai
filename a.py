import os
from dotenv import load_dotenv
import logging

import common
import azurespeechservice
import chatbot
import eventhandler


common.logger_config()
logger = logging.getLogger("file")

def trigger(event_in):
    test = eventhandler.event_handler(event=event_in)
    return test


# if __name__ == "__main__":
#     *args