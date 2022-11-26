#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb 
from .utils import TaurusLongTask
from .data_journal import DataJournal
from .utils import init_kwargs_as_parameters

class Exporter(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @init_kwargs_as_parameters
    def export_network_geojson(self,
                                out_network_filename="out_net.geojson",
                                fields=None, #if none select all fields ; else list of filelds
                                **kwargs):

        number_of_element,=self.one('exporter/count_network')

        features_to_export={}

        def add_field(name,values):
            if features_to_export=={}:
                for start,end,_ in values:
                    features_to_export[(start,end)]={}
            for start,end,value in values:
                features_to_export[(start,end)][name]=value

        if fields == None:
            fields = [f for f, in self.do('exporter/select_network_names')]

        for name in fields:
            values = [(start,end,value) for start,end,value in self.do('exporter/select_network_named_values',{'name':name}) if value is not None]
            # check number of elements
            if len(values) != number_of_element:
                print("skipping field ",name)
                continue

            try:
                float_values=list(map(lambda x:(x[0],x[1],float(x[2])),values))
            except:
                # it is a sql_string
                add_field(name,values)
                continue

            int_values=list(map(lambda x:(x[0],x[1],int(x[2])),float_values))
            if int_values==float_values:
                add_field(name,int_values)
            else:
                add_field(name,float_values)


        geojson={"type": "FeatureCollection","features": []}
        for start,end,linestring in self.do('exporter/select_network_geometry'):
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": eval(linestring)
                    },
                "properties" : features_to_export[(start,end)]
            })

        with open(out_network_filename,'w',encoding='utf-8') as net:
            json.dump(geojson,net)

    @init_kwargs_as_parameters
    def export_od_geojson(self,
                            out_od_filename="out_od.geojson",
                            fields=None, #if none select all fields ; else list of filelds
                            **kwargs):
        number_of_element,=self.one('exporter/count_od')
        features_to_export={}
        def add_field(name,values):
            if features_to_export=={}:
                for od_id,_ in values:
                    features_to_export[od_id]={}
            for od_id,value in values:
                features_to_export[od_id][name]=value

        if fields == None:
            fields = [f for f, in self.do('exporter/select_od_names')]

        for name in fields:
            values = [(od_id,value) for od_id,value in self.do('exporter/select_od_named_values',{'name':name}) if value is not None]

            # check number of elements
            if len(values) != number_of_element:
                print("skipping field ",name)
                continue

            try:
                float_values=list(map(lambda x:(x[0],float(x[1])),values))
            except:
                # it is a sql_string
                add_field(name,values)
                continue

            int_values=list(map(lambda x:(x[0],int(x[1])),float_values))
            if int_values==float_values:
                add_field(name,int_values)
            else:
                add_field(name,float_values)

        geojson={"type": "FeatureCollection","features": []}
        for od_id,point in self.do('exporter/select_od_geometry'):
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": eval(point)
                    },
                "properties" : features_to_export[od_id]
            })

        with open(out_od_filename,'w',encoding='utf-8') as od:
            json.dump(geojson,od)

    @init_kwargs_as_parameters
    def export_motion_exchange_geojson(self,
                                out_filename="motion_exchange.geojson",
                                fields=None, #if none select all fields ; else list of filelds
                                **kwargs):
        
        assert self.table_exists('motion_exchange')

        geojson={"type": "FeatureCollection","features": []}

        for start,end,start_id,end_id,motion_exchange,fraction in self.do('exporter/select_motion_exchange_with_geometry'):
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [eval(start),eval(end)]
                    },
                "properties" : {
                    "start": start_id,
                    "end": end_id,
                    "motion_exchange": motion_exchange,
                    "fraction": fraction
                }
            })

        with open(out_filename,'w',encoding='utf-8') as net:
            json.dump(geojson,net)
        
    @init_kwargs_as_parameters
    def export_network_without_repetition_geojson(self,
                                out_filename="no_repetition_network.geojson",
                                fields=None, #if none select all fields ; else list of filelds
                                **kwargs):
        geojson={"type": "FeatureCollection","features": []}

        for start,end,linestring,count in self.do('exporter/select_network_geometry_without_repetition'):
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": eval(linestring)
                    },
                "properties" : {}
            })

        with open(out_filename,'w',encoding='utf-8') as net:
            json.dump(geojson,net)

    @init_kwargs_as_parameters
    def export_node_zones(self,
                        out_filename="node_zones.geojson",
                        zone_name_prefix="STREFA_",
                        od_field_name="LOC_ID",
                        fields=None, #provide list of fields
                        **kwargs):
        
        property_builder = dict()

        # { 7: { STREFA_4": "4 5 7", ...,LOC_ID: 7}, 9: {"STREFA_3: "4 7 9" ...} ... }
        for od_id,ring,group in self.do('exporter/select_od_rings_orionjs'):
            if od_id not in property_builder:
                property_builder[od_id]={}
            property_builder[od_id][od_field_name]=od_id
            property_builder[od_id][zone_name_prefix+str(ring)]=str(group) if group else None
        
        for i,od_id in enumerate(property_builder):
            property_builder[od_id]['ID']=i

        geojson={"type": "FeatureCollection","features": []}
        for od_id in property_builder:
            geojson["features"].append({
                "type": "Feature",
                "geometry": {"type": "GeometryCollection" , "geometries":[]},
                "properties" : property_builder[od_id]
            })

        with open(out_filename,'w',encoding='utf-8') as od:
            json.dump(geojson,od)

    def export_zones_cost(self,
                        out_filename="zones_cost.geojson",
                        zone_name="ZONE",
                        cost_name="COST",
                        **kwargs):
        
        property_builder = []

        for _,size,prior_cost in self.do('exporter/select_random_ring_layout_costs'):
            property_builder.append({
                'ID':len(property_builder),
                zone_name:prior_cost+size,
                cost_name:prior_cost+size/2
            })

        geojson={"type": "FeatureCollection","features": []}
        for element in property_builder:
            geojson["features"].append({
                "type": "Feature",
                "geometry": {"type": "GeometryCollection" , "geometries":[]},
                "properties" : element
            })

        with open(out_filename,'w',encoding='utf-8') as od:
            json.dump(geojson,od)
