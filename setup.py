#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from distutils.core import setup
from setuptools import setup

setup(
    name='pankus',
    version='1.2',
    packages=[
        'pankus',
    ],
    package_data={
        'pankus': ['SQL/*.sql',
                   'SQL/intopp/*.sql',
                   'SQL/initial/*.sql',
                   'SQL/route/*.sql',
                   'SQL/mst/*.sql',
                   'SQL/analysis/*.sql'
                   ],     # All files from folder
    },
    requires=[
        'progressbar2',
        'numpy',
    ],
    url='http://github.com/mk45/pankus',
    license='(c) Politechnika Wrocławska',
    author='Maciej Kamiński',
    author_email='maciej.kaminski@pwr.edu.pl',
    description='Spatial planning software',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 3',
        'Programming Language :: SQL',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)
