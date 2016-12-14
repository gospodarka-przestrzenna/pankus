#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from ipy_progressbar import ProgressBar


class TaurusLeaf:

    def __init__(self,**kwargs):
        super().__init__()
        self.kwargs=kwargs
        self.if_progressbar=kwargs.get('progressbar',True)

    def _taurus_progressbar(self,iterator):
        if self.if_progressbar:
            return ProgressBar(iterator)
        else:
            return iterator
