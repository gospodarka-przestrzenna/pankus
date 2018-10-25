#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .utils import TaurusLongTask
from .data_journal import DataJournal

class Importer(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs
        self.network_filename=kwargs.get('network_filename','net.geojson')
        self.od_filename=kwargs.get('od_filename','od.geojson')
        self.od_id_name=kwargs.get('od_id_name','od_id')

    def import_network_geojson(self,make_two_side=False):
        self.do('initial/create_network')
        with open(self.network_filename,'r') as net:
            net_data=json.load(net)
            # print(net_data.keys())

            geometry_to_insert=[]
            data_to_insert=[]
            for feature in TaurusLongTask(net_data['features'],**self.kwargs):
                assert 'LineString' == feature['geometry']['type']

                linestring=json.dumps(feature['geometry']['coordinates'])
                start=json.dumps(feature['geometry']['coordinates'][0])
                end=json.dumps(feature['geometry']['coordinates'][-1])

                geometry_to_insert.append({
                    'start':str(start),
                    'end':str(end),
                    'linestring':str(linestring)
                })
                if make_two_side:
                    linestring=json.dumps(list(reversed(feature['geometry']['coordinates'])))
                    geometry_to_insert.append({
                        'start':str(end),
                        'end':str(start),
                        'linestring':str(linestring)
                    })

                for key in feature['properties']:
                    name=key
                    value=feature['properties'][key]
                    data_to_insert.append({
                        'start':str(start),
                        'end':str(end),
                        'name':str(name),
                        'value':str(value)
                    })
                    if make_two_side:
                        data_to_insert.append({
                            'start':str(end),
                            'end':str(start),
                            'name':str(name),
                            'value':str(value)
                        })

            self.transaction('initial/import_network_geometry',geometry_to_insert)
            self.transaction('initial/import_network_properties',data_to_insert)

        if self.table_exists('od_geometry'):
            self.point_from_network_od()
            self.check_geometry()

    def import_od_geojson(self):
        self.do('initial/create_od')
        with open(self.od_filename,'r') as od:
            od_data=json.load(od)

            geometry_to_insert=[]
            data_to_insert=[]
            for feature in TaurusLongTask(od_data['features'],**self.kwargs):
                assert 'Point' == feature['geometry']['type']
                assert self.od_id_name in feature['properties']

                od_id=feature['properties'][self.od_id_name]
                geometry=json.dumps(feature['geometry']['coordinates'])
                geometry_to_insert.append({
                    'od_id':int(od_id),
                    'point':str(geometry)
                })
                for key in feature['properties']:
                    name=key
                    value=feature['properties'][key]
                    data_to_insert.append({
                        'od_id':int(od_id),
                        'name':str(name),
                        'value':str(value)
                    })

            self.transaction('initial/import_od_geometry',geometry_to_insert)
            self.transaction('initial/import_od_properties',data_to_insert)

        if self.table_exists('network_geometry'):
            self.point_from_network_od()
            self.check_geometry()

    def point_from_network_od(self):
        self.do('initial/create_point')
        self.do('initial/insert_point')

    def point_from_od(self):
        self.do('initial/create_point')
        self.do('initial/insert_point_from_od')

    def check_geometry(self):
        for point, in self.do('initial/check_geometry'):
            print("problem with geometry at:", point)
        if not list(self.do('initial/check_geometry')):
            print("No geometry problems")

    def fix_geometry(self,range):
        self.do('initial/fix_geometry',{'range':range})
        self.point_from_network_od()
        self.check_geometry()
