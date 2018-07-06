#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from .sqlite_database import SQLiteDatabase

class Path(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

    def create_path(self,k_path=1):
        if k_path > 1:
            raise NotImplemented
        else:
            assert self.table_exists('distance')
            self.do('')
