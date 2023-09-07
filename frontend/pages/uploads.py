import os
from dotenv import load_dotenv
import streamlit as st
import requests
import json
import time

blob_url = None
audio_transcription = None

load_dotenv()
with st.sidebar:
    upload_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'ogg'],
                                   accept_multiple_files=False)
    locale = st.selectbox('Transcribe Language',('en-US', 'vi-VN'))
    # if not upload_file == []:
    if not upload_file == None:
        upload_btn = st.button('Generate transcript and summarize')
        if upload_btn:
            with st.spinner('Uploading files...'):
                file_endpoint = f'{os.getenv("BACKEND_URL")}/files'
                file_payload = {'file_name': upload_file.name}
                req = requests.post(file_endpoint, params=file_payload, files={'uploaded_file': upload_file.getvalue()})
                blob_url = req.text
                blob_url = req.text.replace('"', '')
                time.sleep(10)

if blob_url is not None:
    def _chat_show(speaker_number, content):
        message = st.chat_message(f'{speaker_number}')
        message.write(content)

    st.header('Audio Transcription')
    with st.spinner('Transcribing...'):
        transcribe_payload = {'blob_url': blob_url, 'locale': locale}
        print(f'transcribe_payload: {transcribe_payload}')
        transcribe_endpoint = f'{os.getenv("BACKEND_URL")}/transcribe'
        headers = {'Content-Type': 'application/json'}
        req = requests.post(transcribe_endpoint, json=transcribe_payload, headers=headers)
        req_json = json.loads(req.text)
        
        status_payload = {'status_url': req_json["self"]}
        transcribe_status_endpoint = f'{transcribe_endpoint}/status'
        req = requests.get(transcribe_status_endpoint, json=status_payload, headers=headers)
        transcribe_status = json.loads(req.text)['status']
        print(f'transcribe_status: {transcribe_status}')
        while not transcribe_status == 'Succeeded':
            time.sleep(10)
            status_payload = {'status_url': req_json["self"]}
            transcribe_status_endpoint = f'{transcribe_endpoint}/status'
            req = requests.get(transcribe_status_endpoint, json=status_payload, headers=headers)
            transcribe_status = json.loads(req.text)['status']
            if transcribe_status == 'Failed':
                e = requests.exceptions.HTTPError('Transcribe Failed')
                st.exception(e)
                break

        if transcribe_status == 'Succeeded':
            files_url = json.loads(req.text)['links']['files']
            files_payload = {'files_url': files_url}
            print(files_payload)
            transcribe_file_endpoint = f'{transcribe_endpoint}/result'
            req = requests.get(transcribe_file_endpoint, json=files_payload, headers=headers)
            audio_transcription_json = req.json()
            audio_transcription_text = req.text

    for convo in audio_transcription_json:
        _chat_show(convo['speaker'], convo['phrase'])

    st.header('Audio Transcription - Corrected by GPT')
    with st.spinner('GPT correcting transcription...'):
        correction_payload = {'text': audio_transcription_text}
        correction_endpoint = f'{os.getenv("BACKEND_URL")}/correction'
        print(f'correction_endpoint: {correction_endpoint}')
        print(f'correction_payload: {correction_payload}')
        req = requests.post(correction_endpoint, json=correction_payload, headers=headers)
        correction_result_json = req.json()
        correction_result_text = req.text
        print(f'correction_result: {correction_result_text}')

    for convo in correction_result_json:
        _chat_show(convo['speaker'], convo['phrase'])

    st.header('Transcription Summarized by GPT')
    with st.spinner('GPT summarizing transcription...'):
        # summarize_payload = {'text': correction_result_text}
        summarize_payload = {'text': correction_result_text, 'language': locale}
        print(summarize_payload)
        summarize_endpoint = f'{os.getenv("BACKEND_URL")}/summarize'
        req = requests.post(summarize_endpoint, json=summarize_payload, headers=headers)
        # summarize_result_json = req.json()
        summarize_result_text = req.text
        summarize_result_text = summarize_result_text.replace('\n', '')
        summarize_result_text = summarize_result_text.replace('<|im_end|>', '')
        st.write(summarize_result_text)

    st.header('Positive Negative Check')
    with st.spinner('GPT sentimenting transcription...'):
        sentiment_payload = {'transcript': correction_result_text, 'summary': summarize_result_text}
        print(f'sentiment_payload: {sentiment_payload}')
        sentiment_endpoint = f'{os.getenv("BACKEND_URL")}/sentiment'
        req = requests.post(sentiment_endpoint, json=sentiment_payload, headers=headers)
        # summarize_result_json = req.json()
        sentiment_result_text = req.text
        print(f'sentiment_result: {sentiment_result_text}')
        st.info(sentiment_result_text)