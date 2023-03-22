import os
import logging
import azure.cognitiveservices.speech as speechsdk

import common


common.logger_config()
logger = logging.getLogger("file")


class SoundFileToText:
    """
    Convert sound file to text
    """

    def __init__(self):
        """
        Setup speech config
        """
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'),
            region=os.getenv('SPEECH_REGION'))
        self.speech_config.speech_recognition_language = "en-US"

    @common.log_function_call
    def convert_to_text(self, audio_file):
        """
        Convert sound file to text
        """
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config)
        try:
            result = speech_recognizer.recognize_once()
            return result.json
        except Exception as err:
            logger.error(err)
            raise err


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    app = SoundFileToText()
    file_path = common.convert_to_realpath("../tests/harvard.wav")
    res = app.convert_to_text(file_path)
    print(res)
