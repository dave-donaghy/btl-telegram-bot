'''
BTL Game Database
'''

import logging

# FIXME Put all of these things into a real database.
LOCATION_WINTER = [-2.379035, 51.407912]

START_MESSAGE = '''
This is the Bath Touch Leagues bot.

Use it to get info about the league and upcoming games.

If you're a captain or ref, you can also use it to record results.

It might even be possible to turn it into a nationwide thing, where
the results you see are always for your local league. Maybe.
'''


class Database():
    '''
    Database for games, results, refs, times etc.
    '''

    def __init__(self):
        '''
        Set up MongoDB connection.
        '''

        self.__logger = logging.getLogger(__name__)

    def add_admin(self, contact):
        '''
        Add a user as an admin.
        '''

        self.__logger.info(f'add_admin({contact}')

    def get_teams(self):
        '''
        Get all teams registered in current league.
        '''

        self.__logger.info('get_teams')
        teams = ['Striders', 'Hornets', 'Rebels', 'Mougars']

        return teams

    def get_games(self):
        '''
        Get data on all upcoming games.
        '''

        games = '''
Striders - Hornets, Tuesday 7 April, 18:30
Rebels - Mougars, Tuesday 7 April, 19:15
Space Invaders - Hawks, Tuesday 7 April, 19:15
'''

        return games

    def get_table(self):
        '''
        Get current league table.
        '''

        table = '''
`Team      | W  D  L |  P `
`-------------------------`
`Striders  | 6  0  0 |  24`
`Hornets   | 5  0  1 |  21`
`Rebels    | 4  0  2 |  18`
'''

        return table

    def get_times(self):
        '''
        Get time slots for current league.
        '''

        times = '''
Tuesdays from May till July 2020
5 pitches.
Slot 1: 18:30 - 19:15
Slot 2: 19:20 - 20:05
Slot 3: 20:10 - 20:55
'''

        return times

    def get_start_message(self):
        '''
        Get start message for bot.
        '''

        self.__logger.info('get_start_message')
        return START_MESSAGE

    def get_venue(self):
        '''
        Get venue for current league.
        '''

        self.__logger.info('get_venue')
        return LOCATION_WINTER, 'Kingswood Upper Sports Field and Pavilion', \
                                'Top of Lansdown, opp Beckford\'s Tower'

    def set_win(self, team):
        '''
        Record a win for the given team in their most recent game.
        '''

        self.__logger.info(f'set_win(\'{team}\')')
