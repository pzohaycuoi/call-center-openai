from unittest import TestCase
from dotenv import load_dotenv
from src.backend import chatbot


class Test(TestCase):

    def test_chatgpt3(self):
        app = chatbot.ChatApp()
        message_list = [
            "I want to know how to learn python quickly?",
            "What are the best resources for this?",
            "what should I learn first?"
        ]
        for m in message_list:
            res = app.chat(m)
            print(m, res)


if __name__ == '__main__':
    load_dotenv()
    a = Test()
    a.test_chatgpt3()
