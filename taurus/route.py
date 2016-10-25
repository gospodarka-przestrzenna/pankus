#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase
from heapq import heappush,heappop
from ipy_progressbar import ProgressBar

class Route(SQLiteDatabase):

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


    # not in this module just for now in here
    def generate_connections(self):
        self.do('create_connection')
        if not self.table_exists('traffic'):
            self.do('insert_connection')
        else:
            # new weight in order of traffic
            pass

    def distance(self):
        #self.generate_connections()
        assert self.one('test_point_id_range')[0]

        self.do('create_distance')

        featured_points=self.do('select_sd_point').fetchall()
        all_points=self.do('select_point').fetchall()

        connections=[{} for p in all_points]
        for start,end,weight, in self.do('select_connection'):
            connections[start][end]=weight

        for _,start,_, in ProgressBar(featured_points):
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

            for end in connections[start]:
                weight=connections[start][end]
                new_distances[end] = {
                    'start_id': start,
                    'end_id': end,
                    'weight': weight,
                    'successor_id': end,
                    'predecessor_id': start
                }
                heappush(H, (weight, end))

            while H != []:

                weight,found = heappop(H)
                if used[found]:
                    continue
                used[found] = True

                for c_end in connections[found]:
                    c_weight = connections[found][c_end]+weight
                    if new_distances[c_end]['weight'] > c_weight:
                        new_distances[c_end]['weight'] = c_weight
                        new_distances[c_end]['successor_id'] = new_distances[found]['successor_id']
                        new_distances[c_end]['predecessor_id'] = found
                        heappush(H,(c_weight, c_end))
            self.transaction('import_distance',new_distances)

        self.commit()