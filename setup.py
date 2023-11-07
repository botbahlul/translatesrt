#!/usr/bin/env python3
from __future__ import unicode_literals
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='setuptools')
warnings.filterwarnings("ignore", category=UserWarning, module='setuptools')
warnings.filterwarnings("ignore", message=".*is deprecated*")

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_version():
    init_file = os.path.join(os.path.dirname(__file__), 'translatesrt', '__init__.py')
    with open(init_file, 'r') as f:
        for line in f:
            if line.startswith('VERSION'):
                return line.split('=')[1].strip().strip('"\'')

long_description = (
    'translatesrt is a utility for translating a subtitle file to another language'
)

install_requires=[
        "pysrt>=1.0.1",
        "progressbar2>=3.34.3",
]

setup(
    name="translatesrt",
    version=get_version(),
    description="a utility for translating a subtitle file to another language",
    long_description = long_description,
    author="Bot Bahlul",
    author_email="bot.bahlul@gmail.com",
    url="https://github.com/botbahlul/translatesrt",
    packages=["translatesrt"],
    entry_points={
        "console_scripts": [
            "translatesrt = translatesrt:main",
        ],
    },
    install_requires=install_requires,
    license=open("LICENSE").read()
)
