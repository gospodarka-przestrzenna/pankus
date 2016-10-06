#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from ipy_progressbar import ProgressBar


class Helpers(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

    def _taurus_progressbar_cursor(self,script):
        if self.kwargs.get('progressbar',True):
            return ProgressBar(self.execute_script(script))
        else:
            return self.execute_script(script)
