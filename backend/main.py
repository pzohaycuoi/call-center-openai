import os
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from src.gptFunctions import GPTHandler
from src.fileHandler import write_to_file, remove_file
from src.blobAction import BlobHandler
from src.audioTranscription import SpeechToText


app = FastAPI()
load_dotenv()
SPEECH_TO_TEXT = SpeechToText(os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_SPEECH_REGION'))
GPT = GPTHandler(endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'), key=os.getenv('AZURE_OPENAI_KEY'),
                chat_deployment=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT'), chat_model=os.getenv('AZURE_OPENAI_CHAT_MODEL'),
                embed_deployment=os.getenv('AZURE_OPENAI_EMBED_DEPLOYMENT'), embed_model=os.getenv('AZURE_OPENAI_EMBED_MODEL'),
                summarize_deployment=os.getenv('AZURE_OPENAI_SUMM_DEPLOYMENT'), summarize_model=os.getenv('AZURE_OPENAI_SUMM_MODEL'))


@app.post('/files')
async def upload_file_to_azure_blob(file_name, uploaded_file: UploadFile):
    file_path = write_to_file(file_name=file_name, file_bytes=uploaded_file)
    blob_handler = BlobHandler(storage_account_name=os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
                               container_name=os.getenv('AZURE_BLOB_CONTAINER_NAME'))
    blob_url = blob_handler.upload_blob(file_path)
    remove_file(file_path)
    return blob_url


class TranscriptionItem(BaseModel):
    blob_url: str
    locale: str

@app.post('/transcribe')
async def transcribe_blob(transcribe_item: TranscriptionItem):
    print(f'transcribe_blob payload {transcribe_item.blob_url}')
    return SPEECH_TO_TEXT.transcribe(transcribe_item.blob_url, locale=transcribe_item.locale)


class TranscriptionStatus(BaseModel):
    status_url: str

@app.get('/transcribe/status')
async def transcribe_status(transcription_status: TranscriptionStatus):
    print(f'transcribe_status payload: {transcription_status}')
    return SPEECH_TO_TEXT.transcribe_status(transcription_status.status_url)


class TranscriptionFiles(BaseModel):
    files_url: str

@app.get('/transcribe/result')
async def transcribe_files(transcription_files: TranscriptionFiles):
    print(f'transcribe_files payload :{transcribe_files}')
    return SPEECH_TO_TEXT.get_transcribe_result(transcription_files.files_url)


class TranscriptionText(BaseModel):
    text: str

@app.post('/correction')
async def gpt_correction(transcription_text: TranscriptionText):
    print(f'gpt_correction payload f{transcription_text}')
    return GPT.correct_transcription(transcription_text.text)

# @app.post('/summarize')
# async def gpt_summarize(text_to_summarize: TranscriptionText):
#     print(f'gpt_summarize payload {text_to_summarize}')
#     return GPT.summarize_text(text_to_summarize.text)

class SummarizeBody(BaseModel):
    text: str
    language: str

@app.post('/summarize')
async def gpt_summarize(text_to_summarize: SummarizeBody):
    print(f'gpt_summarize payload {text_to_summarize}')
    return GPT.summarize_text(input=text_to_summarize.text, language=text_to_summarize.language)


class SentimentBody(BaseModel):
    transcript: str
    summary: str

@app.post('/sentiment')
async def gpt_sentiment(text_to_sentiment: SentimentBody):
    print(f'gpt_summarize payload {text_to_sentiment}')
    return GPT.sentiment_check(transcript=text_to_sentiment.transcript, summary=text_to_sentiment.summary)
