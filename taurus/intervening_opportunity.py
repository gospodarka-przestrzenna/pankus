#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase


class InterveningOpportunity(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs
        self.network_filename=kwargs.get('network_filename','net.geojson')
        self.sd_filename=kwargs.get('sd_filename','sd.geojson')
        self.weight_name=kwargs.get('weight_name','weight')
        self.throughput_name=kwargs.get('throughput_name','throughput')
        self.sources_name=kwargs.get('sources_name','sources')
        self.destinations_name=kwargs.get('destinations_name','destinations')
        self.sd_id_name=kwargs.get('destinations_name','sd_id')
        self.selectivity_name=kwargs.get('selectivity_name','selectivity')


    def create_escape_fraction_selectivity(self,efs):
        destinations_total,=self.do('select_destinations_total')
        selectivity=-math.log(efs)/destinations_total
        self.do('update_sd_selectivity',{'selectivity':selectivity*1000000})

    def build_rings(self,no_of_rings):
        self.do('create_ring')
        max_distance,=self.do('distance_maximum')
        #I don't like solution but is mostly what we expect
        factor=no_of_rings/(max_distance+0.001)
        self.do('insert_ring',{'factor':factor})

    def ring_total(self):
        self.do('create_ring_total')
        self.do('insert_ring_total')

    def motion_exchange(self):
        """
        Test description
        :return: Return value
        """
        self.do('create_motion_exchange')
        iterator=self._taurus_progressbar_cursor('select_for_motion_exchange')
        for s,e,r,d_i,d_p,src,dst,sel in iterator:
            if d_i>0:
                fraction=dst*(math.exp(-sel*d_p/1000000)-math.exp(-sel*(d_i+d_p)/1000000))/d_i
            else:
                fraction=0
            self.do('insert_motion_exchange',{
                'sd_start_id':s,
                'sd_end_id':e,
                'fraction':fraction,
                'motion_exchange':fraction*src
            })

