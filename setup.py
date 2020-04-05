#!/usr/bin/env python

from setuptools import setup

setup(
    name='btl-telegram-bot',
    install_requires = [ 'python-telegram-bot' ],
    entry_points={
        'console_scripts': [
            'btl-telegram-bot = btl.bot:main',
        ],
    }
)
