from telegram.ext import Application, CommandHandler, MessageHandler, filters
from speechkit import Session, SpeechSynthesis, ShortAudioRecognition
from dotenv import load_dotenv
from io import BytesIO
import openai
import os


load_dotenv()

TOKEN = os.environ.get("TOKEN")
GPT_SECRET_KEY = os.environ.get("GPT_SECRET_KEY")
SK_TOKEN = os.environ.get("SK_TOKEN")
CATALOG_ID = os.environ.get("CATALOG_ID")

openai.api_key = GPT_SECRET_KEY

# экземпляр класса `Session` и авторизация по токену и id
session = Session.from_yandex_passport_oauth_token(SK_TOKEN, CATALOG_ID)


async def get_answer(text):
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0301",
        messages=[{"role": "user", "content": text}])
    return completion.choices[0].message["content"]


async def start(update, context):
    await update.message.reply_text('Задайте любой вопрос chatGPT')


async def help_command(update, context):
    await update.message.reply_text("Вы можете пообщаться с chatGPT на любую тему")


async def gpt(update, context):

    # получаем файл аудиосообщения от пользователя
    file = await update.message.voice.get_file()
    byte_voice = await file.download_as_bytearray()

    # экземпляр класса распознавания речи
    recognizeShortAudio = ShortAudioRecognition(session)

    # выполняем распознавание речи
    text = recognizeShortAudio.recognize(BytesIO(byte_voice), sampleRateHertz='48000')

    # отправляем текст в chatGPt
    res = await get_answer(text)

    # Создаем экземляр класса `SpeechSynthesis`, передавая `session`
    synthesizeAudio = SpeechSynthesis(session)
    gen_voice = synthesizeAudio.synthesize_stream(text=res,
                                voice='oksana', 
                                sampleRateHertz='48000')

    await update.message.reply_voice(gen_voice)


def main():

    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("help", help_command, block=False))
    application.add_handler(MessageHandler(filters.VOICE, gpt, block=False))

    # запуск приложения. Для остановки нужно нажать Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()