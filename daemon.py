#!/usr/bin/env python3
# coding: utf8

import pyttsx3
from dotenv import load_dotenv
from kafka.Queue import QueueConsumer
import os

load_dotenv()

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))



queueConsumer = QueueConsumer(os.environ['CLOUDKARAFKA_TOPIC'])
# initialize Text-to-speech engine
#engine = pyttsx3.init()
engine = pyttsx3.init()
change_voice(engine, "es_MX", "VoiceGenderFemale")
engine.say("Hola mundo")
engine.runAndWait()

def callback(msgDict):
    text = "Llegó un mensaje!"
    print(text)
    engine.say(str(msgDict['body']['txt']))
    engine.runAndWait()    
    print(msgDict)


queueConsumer.listen(callback)

