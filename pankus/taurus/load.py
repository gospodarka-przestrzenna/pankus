#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Wawrzyniec Zipser, Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .utils import TaurusLongTask
from .data_journal import DataJournal
from .utils import init_kwargs_as_parameters
from .utils import RouteCache

class Load(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def load_route(self,load_name='load',**kwargs):
        #create load
        assert self.table_exists('connection')
        assert self.table_exists('network_properties')
        assert self.table_exists('point')
        assert self.table_exists('motion_exchange')

        self.do('initial/clean_value_net',{'name':load_name,"new_name":load_name})

        for s,e,f, in  self.do('intopp/select_motion_exchange_fraction'):
            self.do('load/load_connections')
        
        
    
    @init_kwargs_as_parameters
    @DataJournal.log_and_stash("connection")
    def remove_network_having_value(self,key=None,value=None,**kwargs):
        """
        Removes the connections having specfic value in key. Value exists in analog network_properties table

        :param key: The name of the colum to look for a value
        :param value: the value for which connection will be removed
        """
        assert self.table_exists('point')
        assert self.table_exists('connection')
        assert self.table_exists('network_properties')
        self.do('load/remove_network_having_value',{
            'key':key,
            'value':value
        })


    def initialize_load(self,load_name=None,**kwargs):
        """ 
            Creates load table, that holds load for a graph.
        """
        self.do('load/create_load')
        self.do('load/initialize_load',{"load_name":load_name})
        
    @init_kwargs_as_parameters        
    def do_load(self,method="python",fraction=1.0,**kwargs):
        """
        """
        if method=='python':
            
            rc=RouteCache(self)
            rc.cache_motion_exchange()
            rc.cache_load()

            expected_problem_size,=self.do('load/select_path_count').fetchone()

            for start,end,_,sstart,send in TaurusLongTask(\
                                            self.do('load/select_path'),\
                                            max_value=expected_problem_size,\
                                            additional_text='Loading_paths',\
                                            **kwargs):
                if rc.od_id[end]:
                    rc.load[sstart][send]+=rc.motion_exchange[rc.od_id[start]][rc.od_id[end]]*fraction
                    
            load_to_store=[]
            for i,s in enumerate(rc.load):
                for e in rc.load[i]:
                    load_to_store.append({"start_id":i,"end_id":e,"load":rc.load[i][e]})
            self.do('load/delete_load')
            self.transaction('load/import_load',load_to_store)

        elif method=="SQL":
            self.do('load/load_connections',{"fraction":fraction})

    def save_load(self,saved_name='load',**kwargs):
        """
        Saves load to network_parameters
        """
        self.do('initial/clean_value_net',{'name':saved_name,"new_name":saved_name,"default":"0"})
        self.do('load/save_load_to_net',{'name':saved_name})

    @init_kwargs_as_parameters
    def path_and_load(self,fraction=1.0,**kwargs):        
        rc=RouteCache(self)
        rc.cache_motion_exchange()
        rc.cache_load()
        rc.cache_distances()
        

        for start_od_id in TaurusLongTask(\
                        rc.featured_points,\
                        additional_text='Load',\
                        **kwargs):
            
            for _,end_id,_ in rc.points:
                if rc.od_id[end_id]==None:
                    continue
                end_od_id = rc.od_id[end_id]
                
                #if start_od_id==end_od_id:
                #    continue
                # the value will be spread on segments
                value=rc.motion_exchange[start_od_id][end_od_id]
                if not value:
                    continue
                predeccessor = rc.distance[start_od_id][end_id][0]   
                if predeccessor==None:
                    continue
                #save load
                #print(start_od_id)
                #print(predeccessor,end_id)
                #print(rc.load[predeccessor])
                successor=end_id
                while rc.od_id[successor]!=start_od_id:
                    rc.load[predeccessor][successor]+=rc.motion_exchange[start_od_id][end_od_id]*fraction
                    predeccessor,successor=rc.distance[start_od_id][predeccessor][0],predeccessor
                    

        load_to_store=[]
        for i,s in enumerate(rc.load):
            for e in rc.load[i]:
                load_to_store.append({"start_id":i,"end_id":e,"load":rc.load[i][e]})
        self.do('load/delete_load')
        self.transaction('load/import_load',load_to_store)

    @init_kwargs_as_parameters
    def load_cost_connections(self,
            load_name="load",
            throughput_name="throughput",
            cost_name="cost",**kwargs):
        self.do('load/create_cost_load_change')
        self.do('load/initialize_cost_load_change',{
            "load_name":load_name,
            "throughput_name":throughput_name,
            "cost_name":cost_name
        })
        self.do('route/create_connection')
        self.do('load/create_loaded_connection')

        



