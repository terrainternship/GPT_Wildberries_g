from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# telegram token
TOKEN = os.environ.get("TOKEN")

# TODO check this for modular using to switch between llm's (YandexGPT, GigaGPT, HuggingFace ...)
# GPT_SECRET_KEY = os.environ.get("GPT_SECRET_KEY")
# MODEL = os.environ.get("GPT_MODEL")
# openai.api_key = GPT_SECRET_KEY


async def get_answer(text: str, user: str ="user") -> str:
    # completion = await openai.ChatCompletion.acreate(
    #     model=MODEL,
    #     messages=[{"role": user, "content": text}])
    # return completion.choices[0].message["content"]

    # use echo
    return text


async def start(update, context):
    await update.message.reply_text('Задайте любой вопрос')


async def help_command(update, context):
    await update.message.reply_text("Вы можете пообщаться на любую тему")


async def gpt(update, context):
    res = await get_answer(update.message.text)
    await update.message.reply_text(res)


def main():

    application = Application.builder().token(TOKEN).build()
    logging.info('Бот запущен...')

    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("help", help_command, block=False))
    application.add_handler(MessageHandler(filters.TEXT, gpt, block=False))

    application.run_polling()


if __name__ == "__main__":
    main()