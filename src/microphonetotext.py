import os
import azure.cognitiveservices.speech as speechsdk
import common


common.logger_config()


class MicrophoneInput:
    '''
    Create microphone to Azure Speech Service
    Transcribe microphone input to text
    '''
    def __init__(self):
        # Setting Azure Speech Service key and region
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'),
            region=os.getenv('SPEECH_REGION'))
        self.speech_config.speech_recognition_language = "en-US"
        self.audio_config = speechsdk.audio.AudioConfig(
            use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=self.audio_config)

    @common.log_function_call
    def speech_to_text(self):
        '''
        Transcribe microphone speech to text
        '''
        print("Speak into your microphone.")
        speech_recognition_result = self.speech_recognizer.recognize_once_async(
        ).get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {format(speech_recognition_result.text)}")
            return speech_recognition_result.text
        if speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print(
                f"No speech could be recognized: {format(speech_recognition_result.no_match_details)}"
            )
            return False
        if speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print(
                f"Speech Recognition canceled: {format(cancellation_details.reason)}"
            )
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(
                    f"Error details: {format(cancellation_details.error_details)}"
                )
                raise (
                    "Did you set the speech resource key and region values?")
            return False
