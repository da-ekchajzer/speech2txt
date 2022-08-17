#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Speech recognition samples for the Microsoft Cognitive Services Speech SDK
"""

import time

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys

    sys.exit(1)

speech_key, service_region = "a994b4905cc849f0ba3ea3dbb2e9df8e", "francecentral"

# Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16
# kHz).
path = "wav/output.wav"


def speech_recognize_continuous_from_file_2(path, speech_key, service_region):
    """performs continuous speech recognition with input from an audio file"""

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=path)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, language="fr-FR", audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))

    speech_recognizer.recognized.connect(lambda evt: append_file(evt.result.text))

    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    result = speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)


def append_file(line):
    file_object = open('txt/audio.txt', 'a')
    file_object.write(line)
    file_object.close()


if __name__ == '__main__':
    speech_recognize_continuous_from_file_2()
