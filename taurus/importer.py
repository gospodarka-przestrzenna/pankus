#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json
from .sqlite_database import SQLiteDatabase

class Importer(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.network_filename=kwargs.get('network_filename','net.geojson')
        self.sd_filename=kwargs.get('sd_filename','sd.geojson')
        self.weight_name=kwargs.get('weight_name','weight')
        self.throughput_name=kwargs.get('throughput_name','throughput')
        self.sources_name=kwargs.get('sources_name','sources')
        self.destinations_name=kwargs.get('destinations_name','destinations')
        self.sd_id_name=kwargs.get('destinations_name','sd_id')
        self.selectivity_name=kwargs.get('selectivity_name','selectivity')


    def import_network_geojson(self):
        self.execute_script('create_network')
        with open(self.network_filename,'r') as net:
            net_data=json.load(net)
            print(net_data.keys())
            for feature in net_data['features']:
                print(feature)
                assert self.weight_name in feature['properties']
                assert 'LineString' == feature['geometry']['type']

                weight=feature['properties'][self.weight_name]
                throughput=feature['properties'].get(self.throughput_name,'NULL')
                geometry=json.dumps(feature['geometry']['coordinates'])
                start=json.dumps(feature['geometry']['coordinates'][0])
                end=json.dumps(feature['geometry']['coordinates'][-1])

                self.execute_script('import_network',{
                    'linestring':geometry,
                    'weight':weight,
                    'throughput':throughput,
                    'start':start,
                    'end':end
                })


    def import_sd_geojson(self):
        self.execute_script('create_sd')
        with open(self.sd_filename,'r') as sd:
            sd_data=json.load(sd)
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
                self.execute_script('import_sd',{
                    'point':geometry,
                    'sources':sources,
                    'destinations':destinations,
                    'sd_id':sd_id,
                    'selectivity':selectivity
                })
    def point_from_network_sd(self):
        self.execute_script('create_point')
        self.execute_script('insert_point')

    # not in this module just for now in here
    def generate_connections(self):
        pass

