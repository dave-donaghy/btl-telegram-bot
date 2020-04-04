'''
Telegram bot to handle Bath Touch Leagues.

Add this bot to a Telegram group, or speak to it directly,
to add and see fixtures and results.
'''

import logging
import os
import sys

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler
import telegram

LOCATION_WINTER = [51.407912, -2.379035]

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

LOGGER = logging.getLogger(__name__)

def error_handler(update, context):
    '''
    Just log errors.
    '''

    LOGGER.error(f'{type(context.error)}: {context.error}')

def inline_query(update, context):
    '''
    Log each inline query
    '''

    LOGGER.info(f'{update.effective_user.username}: {update.inline_query.query}')

    results = list()
    result = telegram.InlineQueryResultContact(id='Organizer',
                                               cache_time=5,
                                               phone_number='07111222333',
                                               first_name='Dummy',
                                               last_name='Response')
    results.append(result)

    context.bot.answer_inline_query(update.inline_query.id, results=results)

def callback_query(update, context):
    '''
    Log each callback query
    '''

    LOGGER.info(f'Callback from {update.effective_user.username}: {update.callback_query.data}')

    context.bot.answer_callback_query(update.callback_query.id,
                                      text=f'Registered {update.callback_query.data} win.')

def start(update, context):
    '''
    Just recognize a user.
    '''

    LOGGER.info(__name__)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Okay, starting.')

def win(update, context):
    '''
    Record a win, forcing the user to reply with the name of the winning team.

    No details are provided beyond the win; in particular, we do not record scores.
    '''

    LOGGER.info('win')

    teams = ['Striders', 'Hornets', 'Rebels', 'Mougars']
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

    LOGGER.info(__name__)

    games_data = '''
Striders - Hornets, Tuesday 7 April, 18:30
Rebels - Mougars, Tuesday 7 April, 19:15
Space Invaders - Hawks, Tuesday 7 April, 19:15
'''

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=games_data)

def table(update, context):
    '''
    Send the league table.
    '''

    LOGGER.info(__name__)

    table_data = '''
`Team      | W  D  L |  P `
`-------------------------`
`Striders  | 6  0  0 |  24`
`Hornets   | 5  0  1 |  21`
`Rebels    | 4  0  2 |  18`
'''

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=table_data,
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)

def venue(update, context):
    '''
    Send league venue details.
    '''

    LOGGER.info(__name__)

    location = telegram.Location(LOCATION_WINTER[1], LOCATION_WINTER[0])

    venue_data = telegram.Venue(location=location,
                                title='Kingswood Upper Sports Field and Pavilion',
                                address='Top of Lansdown, opp Beckford\'s Tower')

    context.bot.send_venue(chat_id=update.effective_chat.id,
                           venue=venue_data)

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

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('win', win))
    updater.dispatcher.add_handler(CommandHandler('games', games))
    updater.dispatcher.add_handler(CommandHandler('table', table))
    updater.dispatcher.add_handler(CommandHandler('venue', venue))
    updater.dispatcher.add_error_handler(error_handler)

    updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_query))

    updater.start_polling()
