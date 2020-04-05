'''
Telegram bot to handle Bath Touch Leagues.

Add this bot to a Telegram group, or speak to it directly,
to add and see fixtures and results.
'''

import argparse
import logging
import os
import sys

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters

import telegram

import btl.database

def error_handler(_update, context):
    '''
    Just log errors.
    '''

    LOGGER.error(f'{type(context.error)}: {context.error}')

def callback_query(update, context):
    '''
    Log each callback query
    '''

    LOGGER.info(f'win: {update.effective_user.username}: {update.callback_query.data}')

    DATA.set_win(update.callback_query.data)

    context.bot.answer_callback_query(update.callback_query.id,
                                      text=f'Registered {update.callback_query.data} win.')

def contact(update, context):
    '''
    Record a contact message to identify users.
    '''

    LOGGER.info(update.effective_message.contact)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    DATA.add_admin(update.effective_message.contact)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Okay, thanks {update.effective_message.contact.first_name}.')

def captain(update, context):
    '''
    Register a captain.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    contact_key = telegram.KeyboardButton(text='Send contact', request_contact=True)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please add your contact details to register as a captain.',
                             reply_markup=telegram.ReplyKeyboardMarkup([[contact_key]]),
                             one_time_keyboard=True)

def win(update, context):
    '''
    Record a win, forcing the user to reply with the name of the winning team.

    No details are provided beyond the win; in particular, we do not record scores.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    if not DATA.is_admin(update.effective_user.id):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Sorry, only captains and refs can record wins.',
                                 reply_to_message_id=update.effective_message.message_id)

        return

    teams = DATA.get_teams()

    team_buttons = [[telegram.InlineKeyboardButton(text=team,
                                                   callback_data=team) for team in teams]]

    response_keyboard = telegram.InlineKeyboardMarkup(team_buttons)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Which team won?',
                             reply_markup=response_keyboard)

def games(update, context):
    '''
    Send list of next games.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DATA.get_games())

def ref(update, context):
    '''
    Register a referee.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    contact_key = telegram.KeyboardButton(text='Send contact', request_contact=True)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please add your contact details to register as a referee.',
                             reply_markup=telegram.ReplyKeyboardMarkup([[contact_key]]))

def start(update, context):
    '''
    Send start message.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DATA.get_start_message())

def times(update, context):
    '''
    Send general times.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DATA.get_times())

def table(update, context):
    '''
    Send the league table.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DATA.get_table(),
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)

def venue(update, context):
    '''
    Send league venue details.
    '''

    LOGGER.info(update.effective_message.text)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                 action=telegram.ChatAction.TYPING)

    location_gps, title, address = DATA.get_venue()
    location = telegram.Location(location_gps[0], location_gps[1])

    venue_data = telegram.Venue(location=location, title=title, address=address)

    context.bot.send_venue(chat_id=update.effective_chat.id,
                           venue=venue_data)

parser = argparse.ArgumentParser(description='Bath Touch Leagues Telegram bot')
parser.add_argument('--log', help='log file location (defaults to stdout)')
args = parser.parse_args()

if args.log:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=args.log,
                        level=logging.INFO)
else:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

LOGGER = logging.getLogger(__name__)

DATA = btl.database.Database()

def main():
    '''
    Kick off the bot.
    '''

    try:
        updater = Updater(token=os.environ['TELEGRAM_AUTH_TOKEN'],
                          use_context=True)
    except KeyError as error:
        LOGGER.error(error)
        sys.exit(1)

    updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact))

    updater.dispatcher.add_handler(CommandHandler('captain', captain))
    updater.dispatcher.add_handler(CommandHandler('games', games))
    updater.dispatcher.add_handler(CommandHandler('ref', ref))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('table', table))
    updater.dispatcher.add_handler(CommandHandler('times', times))
    updater.dispatcher.add_handler(CommandHandler('venue', venue))
    updater.dispatcher.add_handler(CommandHandler('win', win))

    updater.dispatcher.add_error_handler(error_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(callback_query))

    updater.start_polling()
