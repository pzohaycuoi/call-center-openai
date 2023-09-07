import json
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


class GPTHandler:
    def __init__(self, endpoint: str, key: str, chat_deployment: str, chat_model: str, embed_deployment: str, embed_model: str,
                 summarize_deployment: str, summarize_model: str) -> None:
        self.api_type = 'azure'
        self.api_version = '2023-03-15-preview'
        self.api_base = endpoint
        self.api_key = key
        self.chat_deployment = chat_deployment
        self.chat_model = chat_model
        self.embed_deployment = embed_deployment
        self.embed_model = embed_model
        self.summarize_deployment = summarize_deployment
        self.summarize_model = summarize_model
        self._init_model('chat')
        self._init_model('embed')
        self._init_model('summarize')
        self.prompt_profiles = {
            'transcription_correct': ChatPromptTemplate.from_messages([
                ('system', '''You are a helpful AI assistant, intended to fix any spelling or grammar mistakes in user audio transcript.
                If words appear incorrect or there are run-on word, fix the transcript the best you can.
                If it's a json then please keep that json'''),
                ('human', '{transcription}')
            ]),
            'sentiment': ChatPromptTemplate.from_messages([
                ('system', '''Return a single word sentiment of either ["Positive","Negative" or "Neutral"] from this transcript'''),
                ('human', '''TRANSCRIPT: {transcription}
                TRANSCRIPT SUMMARY: {summary}''')
            ]),
            'summarize': ChatPromptTemplate.from_messages([
                ('system', '''You are a helpful AI assistant, intended to summarize the audio file in call center. 
                we need to understand what is the topic of the call center.
                Answer in {language}'''),
                ('human', '{transcription}')
            ])
        }

    def _init_model(self, model_type: str):
        if model_type == 'chat':
            try:
                self.chat_model = AzureChatOpenAI(openai_api_base=self.api_base, openai_api_key=self.api_key, openai_api_version=self.api_version, 
                                                  deployment_name=self.chat_deployment, model_name=self.chat_model)
            except Exception as err:
                raise(err)
        elif model_type == 'embed':
            try:
                self.embed_model = OpenAIEmbeddings(openai_api_base=self.api_base, openai_api_key=self.api_key, openai_api_version=self.api_version,
                                                    deployment=self.embed_deployment, model=self.embed_model)
            except Exception as err:
                raise(err)
        elif model_type == 'summarize':
            try:
                self.summarize_model = AzureOpenAI(openai_api_base=self.api_base, openai_api_key=self.api_key, openai_api_version=self.api_version,
                                                   openai_api_type=self.api_type, deployment_name=self.summarize_deployment, model_name=self.summarize_model)
            except Exception as err:
                raise(err)
        else: raise ValueError('model_type is not valid')

    def _chat_request(self, prompt):
        try:
            return self.chat_model(prompt).content
        except Exception as err:
            raise(err)

    def correct_transcription(self, transcription: str):
        try:
            correction_prompt = self.prompt_profiles['transcription_correct'].format_messages(transcription=transcription)
            response = self._chat_request(correction_prompt)
            print(f'correct transcription: {response}')
            json_response = json.loads(response)
            return json_response
        except Exception as err:
            raise(err)

    # def summarize_text(self, input):
    #     try:
    #         text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name='gpt-3.5-turbo')
    #         texts = text_splitter.split_text(input)
    #         docs = [Document(page_content=t) for t in texts]
    #         print(f'splitted doc: {docs}')
    #         chain = load_summarize_chain(self.summarize_model, chain_type="stuff")
    #         summarized_text = chain.run(docs)
    #         print(f'summarize: {summarized_text}')
    #         return summarized_text
    #     except Exception as err:
    #         raise(err)

    def summarize_text(self, input: str, language: str):
        try:
            summarize_prompt = self.prompt_profiles['summarize'].format_messages(language=language, transcription=input)
            response = self._chat_request(summarize_prompt)
            print(f'summarize_text: {response}')
            return response
        except Exception as err:
            raise(err)
        
    def sentiment_check(self, transcript: str, summary: str):
        try:
            sentiment_prompt = self.prompt_profiles['sentiment'].format_messages(transcription=transcript, summary=summary)
            response = self._chat_request(sentiment_prompt)
            print(f'sentiment_check: {response}')
            return response
        except Exception as err:
            raise(err)
