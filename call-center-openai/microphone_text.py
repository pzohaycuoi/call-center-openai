import os
import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone(speech_key, speech_region):
    '''
    Request to Azure Speech Service, transcribe microphone input to text
    '''   
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=speech_region)
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                   audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {format(speech_recognition_result.text)}")
        return speech_recognition_result.text
    if speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized: {format(speech_recognition_result.no_match_details)}")
        return False
    if speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print(f"Speech Recognition canceled: {format(cancellation_details.reason)}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {format(cancellation_details.error_details)}")
            print("Did you set the speech resource key and region values?")
            return False
        return False
