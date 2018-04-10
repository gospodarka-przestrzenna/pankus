#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import progressbar

class TaurusLongTask:

    def __init__(self,iterable,**kwargs):
        self.iterator=iter(iterable)
        self.if_progressbar=kwargs.get('progressbar',True)
        if hasattr(iterable, '__len__'):
            self.max_value=len(iterable)
        else:
            self.max_value=kwargs.get('max_value',progressbar.UnknownLength)
        self.additional_text=kwargs.get('additional_text','')
        self.bar_widgets=kwargs.get('progressbar_widgets',\
            [ \
                self.additional_text+' [', progressbar.Timer(), '] ', \
                progressbar.Bar(), \
                ' (', progressbar.ETA(), ') ', \
            ]\
        )


    def __iter__(self):
        if self.if_progressbar:
            self.bar=progressbar.ProgressBar(\
                max_value=self.max_value,\
                widgets=self.bar_widgets,\
            )
            return self
        return self.iterator

    def __next__(self):
        try:
            element = self.iterator.__next__()
            self.bar.update(self.bar.value+1)
            return element
        except Exception as error:
            self.bar.finish()
            raise error

        
