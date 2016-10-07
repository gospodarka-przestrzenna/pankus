#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
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
        self.sd_id_name=kwargs.get('destinations_name','sd_id')
        self.selectivity_name=kwargs.get('selectivity_name','selectivity')


    def import_network_geojson(self):
        self.do('create_network')
        with open(self.network_filename,'r') as net:
            net_data=json.load(net)
            # print(net_data.keys())
            for feature in net_data['features']:
                print(feature)
                assert self.weight_name in feature['properties']
                assert 'LineString' == feature['geometry']['type']

                weight=feature['properties'][self.weight_name]
                throughput=feature['properties'].get(self.throughput_name,'NULL')
                geometry=json.dumps(feature['geometry']['coordinates'])
                start=json.dumps(feature['geometry']['coordinates'][0])
                end=json.dumps(feature['geometry']['coordinates'][-1])

                self.do('import_network',{
                    'linestring':geometry,
                    'weight':weight,
                    'throughput':throughput,
                    'start':start,
                    'end':end
                })

    def import_sd_geojson(self):
        self.do('create_sd')
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
                self.do('import_sd',{
                    'point':geometry,
                    'sources':sources,
                    'destinations':destinations,
                    'sd_id':sd_id,
                    'selectivity':selectivity
                })
    def point_from_network_sd(self):
        self.do('create_point')
        self.do('insert_point')

    # not in this module just for now in here
    def generate_connections(self):
        self.do('create_connection')
        if not self.table_exists('traffic'):
            self.do('insert_connection')
        else:
            # new weight in order of traffic
            pass

    #dendryt function
    def distance(self):
        #self.generate_connections()
        self.do('create_distance')
        sd_point_iterator=self._taurus_progressbar_cursor('select_sd_point')
        for _,_,sd_id in sd_point_iterator:
            self.do('initialize_distance_ring',{'id':sd_id})
            size,=self.do('distance_ring_size')
            while size:
                start_id,end_id,_,_,weight,_=self.do('distance_ring_get_minimum')
                self.do('distance_ring_extend',{
                    'start_id':start_id,
                    'end_id':end_id,
                    'weight':weight
                })
                size,=self.do('distance_ring_size')
                # print(size)

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