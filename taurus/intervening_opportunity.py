#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase
from ipy_progressbar import ProgressBar

class InterveningOpportunity(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

    def create_escape_fraction_selectivity(self,efs):
        destinations_total,=self.one('select_destinations_total')
        selectivity=-math.log(efs)/destinations_total
        self.do('update_sd_selectivity',{'selectivity':selectivity*1000000})

    def build_uniform_rings(self,no_of_rings):
        self.do('create_ring')
        max_distance,=self.one('distance_maximum')
        #I don't like solution but is mostly what we expect
        factor=no_of_rings/(max_distance*1.0001)
        self.do('insert_ring',{'factor':factor})

    def ring_total(self):
        self.do('create_ring_total')
        self.do('insert_ring_total')

    def normalize_motion_exchange(self):
        self.do('normalization')

    def destination_shift(self):
        self.do('destination_shift')

    def general_shift(self):
        self.do('general_shift')

    def sources_shift(self):
        self.do('sources_shift')

    def save_parameters(self,name):
        #sd_id|name|value
        self.table_exists('')

    def motion_exchange(self):
        """
        Test description
        :return: Return value
        """
        self.do('create_motion_exchange')

        featured_points=self.do('select_sd_point').fetchall()
        #iterator for progressbar
        iterator=iter(ProgressBar(range(len(featured_points)**2)))

        motion_exchange=[]
        for start_id,\
            end_id,\
            ring,\
            destinations_in,\
            destinations_prior,\
            sources,\
            destinations,\
            selectivity in self.do('select_for_motion_exchange'):
            #iterator for progressbar
            iterator.__next__()

            if destinations_in>0:
                fraction=destinations*\
                         (math.exp(-selectivity*destinations_prior/1000000)-
                          math.exp(-selectivity*
                                   (destinations_in+destinations_prior)/1000000))/destinations_in
            else:
                fraction=0
            motion_exchange.append({
                'sd_start_id':start_id,
                'sd_end_id':end_id,
                'fraction':fraction,
                'motion_exchange':fraction*sources
            })
        #iterator finished 'nice' (to do)
        for i in iterator:
            pass

        self.transaction('insert_motion_exchange',motion_exchange)
        self.transaction('insert_motion_exchange_fraction',motion_exchange)
        self.commit()



