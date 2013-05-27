#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='',
    version='0.2.0',
    description='life crawler',
    author='modeyangg',
    author_email='modeyangg@gmail.com',
    py_modules=['crawler', ],
    package_data={'': ['LICENSE'], },
    url='https://github.com/modeyang/crawler_Life',
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    install_requires=[
        "BeautifulSoup",
        "sqlalchemy",
        "lxml",
        "pycurl"
    ],
)
