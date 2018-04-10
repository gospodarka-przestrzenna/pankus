#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import progressbar

class TaurusLongTask:

    def __init__(self,iterable,**kwargs):
        self.iterator=iter(iterable)
        self.if_progressbar=kwargs.get('progressbar',True)

    def __iter__(self):
        if self.if_progressbar:
            return self
        return self.iterator

    def __next__(self):
        element = self.iterator.__next__()
        return element
