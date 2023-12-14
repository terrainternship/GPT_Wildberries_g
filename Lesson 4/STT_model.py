from speechkit import Session, ShortAudioRecognition
from dotenv import load_dotenv
import os


load_dotenv()

SK_TOKEN = os.environ.get("SK_TOKEN")
CATALOG_ID = os.environ.get("CATALOG_ID")

# экземпляр класса `Session` и авторизация по токену и id
session = Session.from_yandex_passport_oauth_token(SK_TOKEN, CATALOG_ID)

# читаем аудиофайл
with open('out.wav', 'rb') as f:
    data = f.read()
    
# экземпляр класса распознавания речи
recognizeShortAudio = ShortAudioRecognition(session)

# выполняем распознавание речи
text = recognizeShortAudio.recognize(data, sampleRateHertz='48000')
print(text)