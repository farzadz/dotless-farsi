import os
import boto3
import logging
from dotless import translate
from datetime import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=os.getenv('ACCESS_KEY') or 'some_key', aws_secret_access_key=os.getenv('SECRET_KEY') or 'some_secret')
dynamoClient = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id=os.getenv('ACCESS_KEY') or 'some_key', aws_secret_access_key=os.getenv('SECRET_KEY') or 'some_secret')


class Message:
    def __init__(self, update):
        user = update.message.from_user
        self.message = update.message.text or 'start chat'
        self.user_full_name = user.full_name
        self.username = user.username
    def item(self):
        return {
            'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'message': self.message,
            'username': self.username,
            'userFullName': self.user_full_name
        }
    
def createLogTable():
    if 'BotLogger' not in dynamoClient.list_tables()['TableNames']:
        table = dynamodb.create_table(
    TableName='BotLogger',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH' 
        },
        {
            'AttributeName': 'time',
            'KeyType': 'RANGE'  
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'time',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
    
    return dynamodb.Table('BotLogger')
        
def writeToTable(message, dynamo_table):
    dynamo_table.put_item(Item=message.item())


def start(update, context):
    user = update.message.from_user
    logger.info("Conversation started by user {}, with username {}".format(user.full_name, user.username))
    message = Message(update)
    writeToTable(message, log_table)
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate("سلام! من متن فارسی رو به صورت بی نقطه مینویسم. بهم پیام بده جوابت رو بدون نقطه میدم."))

def translateText(update, context):
    user = update.message.from_user
    message = Message(update)
    writeToTable(message, log_table)
    logger.info("Message {} recieved from user {}, with username {}".format(update.message.text, user.full_name, user.username))
    context.bot.send_message(chat_id=update.effective_chat.id, text=translate(update.message.text))


if __name__ == '__main__':
    log_table = createLogTable()
    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    translate_handler = MessageHandler(Filters.text, translateText)
    dispatcher.add_handler(translate_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()