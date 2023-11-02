from dotenv import load_dotenv
from kafka.Queue import QueueConsumer
import os
from .aia_tts import say, change_voice
from repositories.aiaRepo import AIAMessageRepository
load_dotenv()

queueConsumer = QueueConsumer(os.environ['CLOUDKARAFKA_TOPIC'])
aiaMsgRepo = AIAMessageRepository(os.environ['MONGODB_URI'])

def callback(msgDict):
    #print(msgDict)
    try:
        sentences = msgDict['body']['sentences']
        for sentence in sentences:
            say(sentence)
        aiaMsgRepo.updateAIAMessage(msgDict['id'], "aia-language-engine")
    except KeyError:
        print("[WARN] not body.msg field in message")
        pass

    
    
def startSvc():
    print("start Svc")
    change_voice("es_MX", "VoiceGenderFemale")
    queueConsumer.listen(callback)