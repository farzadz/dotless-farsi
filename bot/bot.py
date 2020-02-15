from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotless import translate
from telegram.ext import MessageHandler, Filters
import os

updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate("سلام! من متن فارسی رو به صورت بی نقطه مینویسم. بهم پیام بده جوابت رو بدون نقطه میدم."))
start_handler = CommandHandler('start', start)

def translateText(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate(update.message.text))

translate_handler = MessageHandler(Filters.text, translateText)
dispatcher.add_handler(translate_handler)
dispatcher.add_handler(start_handler)



updater.start_polling()
