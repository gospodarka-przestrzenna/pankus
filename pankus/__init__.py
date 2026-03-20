#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__authors__ = 'Wawrzynec Zipser, Maciej Kamiński, Wiktor Żelazo - Politechnika Wrocławska'
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pankus")
except PackageNotFoundError:
    __version__ = "4.0"
