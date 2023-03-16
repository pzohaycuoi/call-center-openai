import os
import openai
import backoff
import common


common.logger_config()


class ChatApp:
    '''
    Create ChatGPT conversation
    '''
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
    def chat(self, message):
        '''
        Append the message so it looks like the conversation is continue
        '''
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=self.messages)
        # TODO: handling token count
        self.messages.append({
            "role": "assistant",
            "content": response["choices"][0]["message"].content
        })
        print(response["choices"][0]["message"].content)
        return self.messages, response
