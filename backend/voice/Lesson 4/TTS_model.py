from speechkit import Session, SpeechSynthesis
from dotenv import load_dotenv
import os


load_dotenv()

SK_TOKEN = os.environ.get("SK_TOKEN")
CATALOG_ID = os.environ.get("CATALOG_ID")

# экземпляр класса `Session` и автоизация по токену и id
session = Session.from_yandex_passport_oauth_token(SK_TOKEN, CATALOG_ID)

# создаем экземляр класса `SpeechSynthesis`, передавая `session`
synthesizeAudio = SpeechSynthesis(session)
synthesizeAudio.synthesize('out.wav',
                            text='Привет. Это тестовый прогон речи.',
                            voice='oksana', 
                            sampleRateHertz='48000')
