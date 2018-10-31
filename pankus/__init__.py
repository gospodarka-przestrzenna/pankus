#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__authors__ = 'Maciej Kamiński, Wiktor Żelazo - Politechnika Wrocławska'
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "ERROR"
