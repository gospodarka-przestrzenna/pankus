#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .sqlite_database import SQLiteDatabase

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
        self.sd_id_name=kwargs.get('sd_id_name','sd_id')
        self.selectivity_name=kwargs.get('selectivity_name','selectivity')
        self.convolution_start_name=kwargs.get('convolution_start_name','conv_a')
        self.convolution_size_name=kwargs.get('convolution_size_name','conv_b')
        self.convolution_intensity_name=kwargs.get('convolution_intensity_name','conv_alpha')


    def import_network_geojson(self):
        self.do('initial/create_network')
        with open(self.network_filename,'r') as net:
            net_data=json.load(net)
            # print(net_data.keys())

            data_to_insert=[]
            for feature in net_data['features']:
                # print(feature)
                assert self.weight_name in feature['properties']
                assert 'LineString' == feature['geometry']['type']

                weight=feature['properties'][self.weight_name]
                throughput=feature['properties'].get(self.throughput_name,'NULL')
                geometry=json.dumps(feature['geometry']['coordinates'])
                start=json.dumps(feature['geometry']['coordinates'][0])
                end=json.dumps(feature['geometry']['coordinates'][-1])
                convolution_start=feature['properties'].get(self.convolution_start_name,'NULL')
                convolution_size=feature['properties'].get(self.convolution_size_name,'NULL')
                convolution_intensity=feature['properties'].get(self.convolution_intensity_name,'NULL')

                data_to_insert.append({
                    'linestring':str(geometry),
                    'weight':weight,
                    'throughput':throughput,
                    'start':str(start),
                    'end':str(end),
                    'convolution_start':convolution_start,
                    'convolution_size':convolution_size,
                    'convolution_intensity':convolution_intensity
                })
            self.transaction('initial/import_network',data_to_insert)
        if self.table_exists('sd'):
            self.point_from_network_sd()



    def import_sd_geojson(self):
        self.do('initial/create_sd')
        with open(self.sd_filename,'r') as sd:
            sd_data=json.load(sd)

            data_to_insert=[]
            for feature in sd_data['features']:

                assert self.sources_name in feature['properties']
                assert self.destinations_name in feature['properties']
                assert self.sd_id_name in feature['properties']
                assert 'Point' == feature['geometry']['type']
                selectivity=feature['properties'].get(self.selectivity_name,'NULL')
                convolution_start=feature['properties'].get(self.convolution_start_name,'NULL')
                convolution_size=feature['properties'].get(self.convolution_size_name,'NULL')
                convolution_intensity=feature['properties'].get(self.convolution_intensity_name,0)

                sources=feature['properties'][self.sources_name]
                destinations=feature['properties'][self.destinations_name]
                sd_id=feature['properties'][self.sd_id_name]

                geometry=json.dumps(feature['geometry']['coordinates'])
                data_to_insert.append({
                    'sd_id':int(sd_id),
                    'point':str(geometry),
                    'sources':sources,
                    'destinations':destinations,
                    'selectivity':selectivity,
                    'convolution_start':convolution_start,
                    'convolution_size':convolution_size,
                    'convolution_intensity':convolution_intensity
                })

            self.transaction('initial/import_sd',data_to_insert)

        if self.table_exists('network'):
            self.point_from_network_sd()

    def point_from_network_sd(self):
        self.do('initial/create_point')
        self.do('initial/insert_point')
