import os
import logging
import openai
import backoff
import common


common.logger_config()
logger = logging.getLogger("file")


class ChatApp:
    """
    ChatGPT conversation
    """

    def __init__(self):
        # Setting the API key to use the OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = [
            {
                "role": "system",
                "content": "You are a wealth of knowledge."
            },
        ]

    @common.log_function_call
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def chat(self, message, retain: bool = True):
        '''
        Make request to ChatGPT
        '''
        self.messages.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages)
        except openai.InvalidRequestError as err:
            logger.error(err)
            raise err

        if retain:
            # Append the message for next request context
            self.messages.append({
                "role":
                "assistant",
                "content":
                response["choices"][0]["message"].content
            })
        return response


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    while True:
        app = ChatApp()
        mess = input("Input text here: ")
        res = app.chat(mess)
        response_text = res["choices"][0]["message"].content
        print(f"CHATGPT: {response_text}")
