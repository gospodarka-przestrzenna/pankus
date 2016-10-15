#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .sqlite_database import SQLiteDatabase
from ipy_progressbar import ProgressBar

class Importer(SQLiteDatabase):

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


    def import_network_geojson(self):
        self.do('create_network')
        with open(self.network_filename,'r') as net:
            net_data=json.load(net)
            # print(net_data.keys())

            data_to_insert=[]
            for feature in ProgressBar(net_data['features']):
                # print(feature)
                assert self.weight_name in feature['properties']
                assert 'LineString' == feature['geometry']['type']

                weight=feature['properties'][self.weight_name]
                throughput=feature['properties'].get(self.throughput_name,'NULL')
                geometry=json.dumps(feature['geometry']['coordinates'])
                start=json.dumps(feature['geometry']['coordinates'][0])
                end=json.dumps(feature['geometry']['coordinates'][-1])
                data_to_insert.append({
                    'linestring':str(geometry),
                    'weight':weight,
                    'throughput':throughput,
                    'start':str(start),
                    'end':str(end)
                })
            self.do('import_network',data_to_insert)


    def import_sd_geojson(self):
        self.do('create_sd')
        with open(self.sd_filename,'r') as sd:
            sd_data=json.load(sd)

            data_to_insert=[]
            for feature in sd_data['features']:

                assert self.sources_name in feature['properties']
                assert self.destinations_name in feature['properties']
                assert self.sd_id_name in feature['properties']
                assert 'Point' == feature['geometry']['type']
                selectivity=feature['properties'].get(self.selectivity_name,'NULL')

                sources=feature['properties'][self.sources_name]
                destinations=feature['properties'][self.destinations_name]
                sd_id=feature['properties'][self.sd_id_name]

                geometry=json.dumps(feature['geometry']['coordinates'])
                data_to_insert.append({
                    'point':str(geometry),
                    'sources':sources,
                    'destinations':destinations,
                    'sd_id':sd_id,
                    'selectivity':selectivity
                })

            self.do('import_sd',data_to_insert)
            #self.db_connection.commit()


    def point_from_network_sd(self):
        self.do('create_point')
        self.do('insert_point')
