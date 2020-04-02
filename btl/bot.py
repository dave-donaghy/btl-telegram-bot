'''
Telegram bot to handle Bath Touch Leagues.

Add this bot to a Telegram group, or speak to it directly,
to add and see fixtures and results.
'''

import os

from telegram.ext import Updater
from telegram.ext import CommandHandler

UPDATER = Updater(token=os.environ['TELEGRAM_AUTH_TOKEN'], use_context=True)

DISPATCHER = UPDATER.dispatcher

def start(update, context):
    '''
    Just recognize a user.
    '''

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Okay, starting.')

def hello(update, context):
    '''
    Respond to hello messages. No real functionality.
    '''

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Hello {update.effective_message.from_user.first_name}',
                             reply_to_message_id=update.effective_message.message_id)

def main():
    '''
    Kick off the whole bot.
    '''

    DISPATCHER.add_handler(CommandHandler('hello', hello))
    DISPATCHER.add_handler(CommandHandler('start', start))

    UPDATER.start_polling()
