#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='taurus',
    version='1.0',
    packages=[
        'taurus',
    ],
    package_data={
        'taurus': ['SQL/*.sql'],     # All files from folder A
    },
    requires=[
        'ipy_progressbar',
    ],
    url='http://github.com/mk45/taurus',
    license='(c) Politechnika Wroclawska',
    author='Maciej Kamiński',
    author_email='maciej.kaminski@pwr.edu.pl',
    description='Spatial planning software'

)
