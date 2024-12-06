#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Wawrzyniec Zipser, Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .utils import TaurusLongTask
from .data_journal import DataJournal
from .utils import init_kwargs_as_parameters

class Importer(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def _check_crs_match(self,json_data):
        self.do('initial/create_metadata') # create metadata table if not exists
        
        crs = json_data['crs']
        if crs is None:
            crs_name = 'EPSG:4326'
        else:
            if crs['type'] != 'name':
                raise ValueError("Unsupported crs type "+str(crs))
            else:
                crs_name=crs['properties']['name']

        db_crs = self.one('initial/select_metadata',{'key':'crs_name'})
        if db_crs is None:
            self.do('initial/insert_metadata',{'key':'crs_name','value':crs_name})
        else:
            if db_crs[0] != crs_name:
                raise AssertionError("CRS mismatch: "+str(db_crs[0])+" != "+str(crs_name))
    
    @init_kwargs_as_parameters
    def import_network_geojson(self,
                                make_two_side=False,
                                network_filename="net.geojson",

                                **kwargs):
        self.do('initial/create_metadata')
        self.do('initial/create_network')
        with open(network_filename,'rb') as net:
            net_data=json.load(net)
            
            self._check_crs_match(net_data)
            
            geometry_to_insert=[]
            data_to_insert=[]
            for feature in TaurusLongTask(net_data['features'],**kwargs):
                if "MultiLineString" == feature['geometry']['type']:
                    if len(feature['geometry']['coordinates'])!=1:
                        raise ValueError("Geometry error in feature "+str(feature))
                    geometry = feature['geometry']['coordinates'][0]
                elif 'LineString' == feature['geometry']['type']:
                    geometry = feature['geometry']['coordinates']
                else:
                    raise ValueError("Unsupported geomety in feature "+str(feature))
                
                # chech if geometry is not empty
                if len(geometry)<2:
                    raise ValueError("Empty geometry in feature "+str(feature))
                
                # check if it is not true that each point is the same
                if all([geometry[0]==point for point in geometry]):
                    raise ValueError("All points are the same in feature "+str(feature))

                linestring=json.dumps(geometry)
                start=json.dumps(geometry[0])
                end=json.dumps(geometry[-1])

                geometry_to_insert.append({
                    'start':str(start),
                    'end':str(end),
                    'linestring':str(linestring)
                })
                if make_two_side:
                    linestring=json.dumps(list(reversed(geometry)))
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

    @init_kwargs_as_parameters
    def import_od_geojson(self,od_filename="od.geojson",od_id_name="od_id",**kwargs):
        self.do('initial/create_od')
        with open(od_filename,'rb') as od:
            od_data=json.load(od)
            
            self._check_crs_match(od_data)

            geometry_to_insert=[]
            data_to_insert=[]
            for feature in TaurusLongTask(od_data['features'],**kwargs):
                assert 'Point' == feature['geometry']['type']
                assert od_id_name in feature['properties']

                od_id=feature['properties'][od_id_name]
                geometry=json.dumps(feature['geometry']['coordinates'])
                # check if geometry is not empty
                if len(geometry)!=2:
                    raise ValueError("Empty geometry in feature "+str(feature))
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

    @init_kwargs_as_parameters
    def check_geometry(self,**kwargs):
        #Check lines

        header_printed=False
        for start,end,count in self.do('initial/check_lines'):
            if not header_printed:
                print("Comment, Line_As_WKT")
                header_printed=True
            start=json.loads(start)
            end=json.loads(end)
            print("Problem: multiple connections betweeen two nodes:, \"LINESTRING("+' '.join(map(str,start))+', '+' '.join(map(str,end))+")\"")
        #Check geometry points

        header_printed=False
        for point, in self.do('initial/check_geometry'):
            if not header_printed:
                print("Comment, Point_As_WKT")
                header_printed=True
            point=json.loads(point)
            print("Problem: generating node connection at:, \"POINT("+' '.join(map(str,point))+")\"")
        if not list(self.do('initial/check_geometry')):
            print("No points problems")

    @init_kwargs_as_parameters
    def fix_geometry(self,range=0.01,**kwargs):
        print("Snapping to grid and checking for problems")
        self.do('initial/fix_geometry',{'range':range})
        self.point_from_network_od()
        self.check_geometry()
