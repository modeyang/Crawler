#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='Crawler',
    version='0.2.0',
    description='life crawler',
    author='modeyangg',
    author_email='modeyangg@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    # entry_points = {
    #     'console_scripts' : [
    #         'demo = demo.hello:hello'
    #     ],
    # },
    # package_data={'': ['LICENSE'], },
    url='https://github.com/modeyang/crawler_Life',
    long_description=open('README.md').read(),
    install_requires=[
        "BeautifulSoup",
        "sqlalchemy",
        "lxml",
        "pycurl"
    ],
)
