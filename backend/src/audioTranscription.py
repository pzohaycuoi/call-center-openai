import os
import requests
import json
from urllib.parse import urlparse


class SpeechToText:
    def __init__(self, speech_key: str, speech_region: str) -> None:
        self.speech_key = speech_key
        self.speech_region = speech_region
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.speech_key,
            'Content-Type': 'application/json'
        }

    def transcribe(self, blob_url: str, locale: str) -> requests.Response():
        def _extract_blob_name(blob_url: str) -> str:
            url_compos = urlparse(blob_url)
            return os.path.split(url_compos[2])[1]

        payload = {
            'contentUrls': [f'{blob_url}'],
            'displayName': _extract_blob_name(blob_url=blob_url),
            'locale': locale,
            'properties': {
                "diarizationEnabled": True,
            }
        }
        print(f'transcribe payload: {payload}')
        url = f'https://{self.speech_region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions'
        req = requests.post(url, headers=self.headers, json=payload)
        print(f'Transcribe request: {req.text}')
        req.raise_for_status()
        return req.json()
    
    def transcribe_status(self, transcription_status_url: str):
        req = requests.get(transcription_status_url, headers=self.headers)
        print(f'transcribe status response: {req.text}')
        req.raise_for_status()
        return req.json()
    
    def _get_transcription_files_url(self, transcription_file_url: str):
        req = requests.get(transcription_file_url, headers=self.headers)
        print(f'get transcription files url: {req.text}')
        req.raise_for_status()
        return req.json()
    
    def _get_transcription_content(self, transcription_file_content_url: str):
        req = requests.get(transcription_file_content_url)
        req.raise_for_status()
        req_json = req.json()
        print(f'Transcription file content {req_json}')
        content = []
        try:
            for phrase in req_json['recognizedPhrases']:
                speaker = phrase['speaker']
                display_pharse = phrase['nBest'][0]['display']
                extracted_phrase = {'speaker': speaker, 'phrase': display_pharse}
                print(extracted_phrase)
                content.append(extracted_phrase)
            return content
        except Exception as err:
            raise(err)
    
    def get_transcribe_result(self, transcription_files_url: str):
        files = self._get_transcription_files_url(transcription_files_url)
        transcription_file_url = files['values'][0]['links']['contentUrl']
        transcription_content = self._get_transcription_content(transcription_file_url)
        print(f'transcription_content: {transcription_content}')
        return transcription_content