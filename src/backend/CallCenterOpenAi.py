from os import getenv
from dotenv import load_dotenv

import microphonetotext
import common
import chatbot


common.logger_config()
load_dotenv()
init_microphone = microphonetotext.MicrophoneInput()
init_chatapp = chatbot.ChatApp()
while True:
    cmd_input = input("Press Q to exit, Enter to continue: ")
    if cmd_input == "q":
        break
    text = init_microphone.speech_to_text()
    if text is False:
        continue
    result = init_chatapp.chat(text)
