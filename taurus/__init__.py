#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'
__all__ = [
    'Taurus'
]

from .sqlite_database import SQLiteDatabase
from .importer import Importer

class Taurus(Importer):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)


