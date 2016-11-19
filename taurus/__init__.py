#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'
__all__ = [
    'Taurus'
]

from .sqlite_database import SQLiteDatabase
from .importer import Importer
from .route import Route
from .intervening_opportunity import InterveningOpportunity
from .mst import MST

class Taurus(Importer,Route,InterveningOpportunity,MST):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
