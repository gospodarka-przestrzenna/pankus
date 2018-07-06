#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'
__all__ = [
    'Taurus'
]

from .sqlite_database import SQLiteDatabase
from .importer import Importer
from .route import Route
from .intervening_opportunities import InterveningOpportunities
from .mst import MST
from .network_generators import NetworkGenerator
from .analysis import Analysis

class Taurus(Route,InterveningOpportunities,MST,NetworkGenerator,Analysis):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
