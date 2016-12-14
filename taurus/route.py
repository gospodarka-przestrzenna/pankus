#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase
from .taurus_leaf import TaurusLeaf
from heapq import heappush,heappop
from ipy_progressbar import ProgressBar

class Route(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs
        self.weight_name=kwargs.get('weight_name','weight')
        self.throughput_name=kwargs.get('throughput_name','throughput')


    # not in this module just for now in here
    def generate_connections(self):
        self.do('route/create_connection')
        self.do('route/insert_connection',{
            'weight_name':self.weight_name
        })

    def distance(self):
        #self.generate_connections()
        assert self.one('route/test_point_id_range')[0]
        self.do('route/create_distance')

        featured_points=self.do('route/select_sd_point').fetchall()
        all_points=self.do('route/select_point').fetchall()

        connections=[{} for _ in all_points]
        for start,end,weight, in self.do('route/select_connection'):
            connections[start][end]=weight

        for _,start,_, in self._taurus_progressbar(featured_points):
            #heap
            H=[]
            new_distances = [{
               'start_id': start,
               'end_id': i,
               'weight': float('inf'),
               'successor_id': None,
               'predecessor_id': None
            } for _,i,_, in all_points]

            used=[False for _ in all_points]
            new_distances[start]['weight'] = 0
            new_distances[start]['predecessor_id'] = start
            new_distances[start]['successor_id'] = start
            used[start] = True

            for end,weight in connections[start].items():
                new_distances[end]['weight'] = weight
                new_distances[end]['successor_id'] = end
                new_distances[end]['predecessor_id'] = start
                heappush(H, (weight, end))

            while H != []:

                weight,closest_end = heappop(H)
                if used[closest_end]:
                    continue

                used[closest_end] = True

                for n_end,c_weight in connections[closest_end].items():
                    if used[n_end]:
                        continue
                    n_weight = c_weight+weight
                    if new_distances[n_end]['weight'] > n_weight:
                        new_distances[n_end]['weight'] = n_weight
                        new_distances[n_end]['successor_id'] = new_distances[closest_end]['successor_id']
                        new_distances[n_end]['predecessor_id'] = closest_end
                        heappush(H,(n_weight, n_end))
            self.transaction('route/import_distance',new_distances)
        self.commit()
