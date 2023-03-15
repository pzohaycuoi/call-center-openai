import os
import openai


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
        return response
