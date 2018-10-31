#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from distutils.core import setup
from setuptools import setup, find_packages
from pankus import __version__, __authors__

setup(
    name='pankus',
    packages=find_packages(),
    include_package_data=True,
    version=__version__,
    authors=__authors__,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'progressbar2',
        'numpy',
        'vincenty',
    ],
    url='http://github.com/mk45/pankus',
    license='(c) Politechnika Wrocławska',
    #author='Maciej Kamiński',
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
