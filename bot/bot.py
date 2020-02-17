from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotless import translate
from telegram.ext import MessageHandler, Filters
import os
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)


updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    user = update.message.from_user
    logger.info("Conversation started by user {}, with username {}".format(user.full_name, user.username))
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate("سلام! من متن فارسی رو به صورت بی نقطه مینویسم. بهم پیام بده جوابت رو بدون نقطه میدم."))

def translateText(update, context):
    user = update.message.from_user
    logger.info("Message {} recieved from user {}, with username {}".format(update.message.text, user.full_name, user.username))
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate(update.message.text))

start_handler = CommandHandler('start', start)
translate_handler = MessageHandler(Filters.text, translateText)
dispatcher.add_handler(translate_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
