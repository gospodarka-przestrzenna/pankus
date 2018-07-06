#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

#from ipy_progressbar import ProgressBar
from .sqlite_database import SQLiteDatabase
import numpy as np
from .importer import Importer

class Analysis(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

    def solve_for_sources(self):
        '''
        Let A*S=D where D - destination satisfied vector A - motion exchange matrix and S - sources vector.
        This function solves S=A\D.

        Stores output in parameters table.
        '''
        assert self.one('route/test_point_id_range')[0]
        featured_points=self.do('route/select_sd_point').fetchall()

        # get mx matrix
        motion_exchange=[[0.0 for j in featured_points] for i in featured_points]
        for s,e,f, in  self.do('intopp/select_motion_exchange_fraction'):
            motion_exchange[s][e]=f

        # get destinations
        destinations_list=[0.0 for i in featured_points]
        for sd_id,_,destinations,_,_,_,_, in self.do('intopp/select_model_parameters').fetchall():
            destinations_list[sd_id]=destinations

        #create matrix and solve
        matrix=np.array(motion_exchange)
        sources_list_=np.linalg.solve(matrix.transpose(),destinations_list)

        #solution accuracy
        accuracy = (np.linalg.cond(matrix)*np.finfo(float).eps)

        # save solutions

        new_sources_value=[{
                "sd_id":i,
                "sources":sources
            } for i,sources in enumerate(sources_list_)]
        self.transaction("analysis/update_sources",new_sources_value)
        return accuracy