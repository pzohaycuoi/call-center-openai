import unittest
import chatbot
import azurespeechservice
import common


class Test(unittest.TestCase):
    def test_chatbot(self):
        """
        Test chatbot
        """
        app = chatbot.ChatApp()
        message_list = [
            "I want to know how to learn python quickly?",
            "What are the best resources for this?",
            "what should I learn first?"
        ]
        for m in message_list:
            res = app.chat(m)
            print(m, res)

    def test_azurespeechservice(self):
        """
        test azure speech service
        """
        app = azurespeechservice.SoundFileToText()
        sound_file = common.convert_to_realpath("./hardvard.wav")
        res = app.convert_to_text(sound_file)
        print(res)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    unittest.main()
