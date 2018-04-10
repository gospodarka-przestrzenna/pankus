#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

class TaurusLeaf:

    def __init__(self,**kwargs):
        super().__init__()
        self.kwargs=kwargs
        self.if_progressbar=kwargs.get('progressbar',True)

    def _taurus_progressbar(self,iterator):
        return iterator
