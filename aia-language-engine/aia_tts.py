#import pyttsx3

#engine = pyttsx3.init()
import torch
from TTS.api import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import time
import pyaudio
import numpy as np
from nltk.tokenize import sent_tokenize
from .aia_sounds import AudioFile
import os

path = "/usr/local/lib/python3.11/site-packages/TTS/.models.json"
model_manager = ModelManager(path)
model_path, config_path, model_item = model_manager.download_model("tts_models/es/mai/tacotron2-DDC")
voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])
syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

fs = 24000  # sampling rate, Hz, must be integer
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(language, gender='VoiceGenderFemale'):
    print("change voice")
#    for voice in engine.getProperty('voices'):
#        if language in voice.languages and gender == voice.gender:
#            engine.setProperty('voice', voice.id)
#            return True

    #raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
#https://api.cloudkarafka.com/console/39f315c8-fde4-440a-a979-f86ee1b46343/browser?topic=1xpbgxp5-yai
#{"body": {"sentences": [{"msg": "Gracias por la rica comida", "sound_in": "transition01.wav"}, {"msg": "te voy a mandar a comprar una bebida cocacola, por que me gusta muchísimo!!!!!"}]}}
def say(sentence):
    start_time = time.time()
    print(sentence)
    wavSentence = syn.tts(sentence["msg"])
    try:
        cwd = os.getcwd()
        print(cwd)
        sound_in = cwd+"/resources/sounds/" + sentence['sound_in']
        audioIn = AudioFile(sound_in)
        audioIn.play()
        audioIn.close()
    except KeyError:
        pass
    npWav = np.array(wavSentence)
    dataSampl = npWav.astype(np.float32).tostring()
    stream.write(dataSampl)

    
    #play stream  
    #while data:  
    #    stream.write(data)  
    #    data = f.readframes(1024)  
    
    #stream.close()
    #wav = syn.tts(txt)
    #syn.save_wav(wav, "target/say2.wav")
    
    print("Speack for {:.2f} seconds".format(time.time() - start_time))
    #stream.stop_stream()
#    engine.say(txt)
#    engine.runAndWait()