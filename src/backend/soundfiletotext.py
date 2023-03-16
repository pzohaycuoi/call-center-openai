import os
import azure.cognitiveservices.speech as speechsdk
import common


common.log_function_call()


class SoundToText:
  def __init__(self):
    