import openai


def chat_completion(org_id, api_key, content: str):
    '''
    ChatGPT request for completion
    '''
    openai.organization = org_id
    openai.api_key = api_key
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ]
    )
    return result
