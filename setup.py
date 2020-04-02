#!/usr/bin/env python

from setuptools import setup

setup(
    name='telegram-bot',
    install_requires = [ 'python-telegram-bot' ],
    entry_points={
        'console_scripts': [
            'telegram-bot = btl.bot:main',
        ],
    }
)
