#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from .data_journal import DataJournal
from .utils import TaurusLongTask
from .utils import init_kwargs_as_parameters


class Path:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @init_kwargs_as_parameters
    @DataJournal.log_and_stash("path")
    def create_path(self,k_path=1,**kwargs):
        if k_path > 1:
            raise NotImplemented
        else:
            assert self.table_exists('distance')
            self.do('path/create_path')
            featured_points=self.do('route/select_od_point').fetchall()

            for _,start,_, in TaurusLongTask(\
                            featured_points,\
                            additional_text='Paths',\
                            **kwargs):
            	self.do('path/create_path_for_od_point',{'start':start})

