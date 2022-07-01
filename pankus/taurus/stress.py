#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .utils import TaurusLongTask
from .data_journal import DataJournal
from .utils import init_kwargs_as_parameters
from .utils import RouteCache

class Stress(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def stress_route(self,stress_name='stress',**kwargs):
        #create stress
        assert self.table_exists('connection')
        assert self.table_exists('network_properties')
        assert self.table_exists('point')
        assert self.table_exists('motion_exchange')

        self.do('initial/clean_value_net',{'name':stress_name,"new_name":stress_name})

        for s,e,f, in  self.do('intopp/select_motion_exchange_fraction'):
            self.do('stress/stress_connections')
        
        
    
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
        self.do('stress/remove_network_having_value',{
            'key':key,
            'value':value
        })


    def initialize_stress(self,stress_name=None,**kwargs):
        """ 
            Creates stress table, that holds stress for a graph.
        """
        self.do('stress/create_stress')
        self.do('stress/initialize_stress',{"stress_name":stress_name})
        
    @init_kwargs_as_parameters        
    def do_stress(self,method="python",fraction=1.0,**kwargs):
        """
        """
        if method=='python':
            
            rc=RouteCache(self)
            rc.cache_motion_exchange()
            rc.cache_stress()

            expected_problem_size,=self.do('stress/select_path_count').fetchone()

            for start,end,_,sstart,send in TaurusLongTask(\
                                            self.do('stress/select_path'),\
                                            max_value=expected_problem_size,\
                                            additional_text='Stressing',\
                                            **kwargs):
                if rc.od_id[end]:
                    rc.stress[sstart][send]+=rc.motion_exchange[rc.od_id[start]][rc.od_id[end]]*fraction
                    
            stress_to_store=[]
            for i,s in enumerate(rc.stress):
                for e in rc.stress[i]:
                    stress_to_store.append({"start_id":i,"end_id":e,"stress":rc.stress[i][e]})
            self.do('stress/delete_stress')
            self.transaction('stress/import_stress',stress_to_store)

        elif method=="SQL":
            self.do('stress/stress_connections',{"fraction":fraction})

    def save_stress(self,saved_name='stress',**kwargs):
        """
        Saves stress to network_parameters
        """
        self.do('initial/clean_value_net',{'name':saved_name,"new_name":saved_name,"default":"0"})
        self.do('stress/save_stress_to_net',{'name':saved_name})

    @init_kwargs_as_parameters
    def path_and_stress(self,fraction=1.0,**kwargs):        
        rc=RouteCache(self)
        rc.cache_motion_exchange()
        rc.cache_stress()
        rc.cache_distances()
        

        for start_od_id in TaurusLongTask(\
                        rc.featured_points,\
                        additional_text='Stress',\
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
                #save stress
                #print(start_od_id)
                #print(predeccessor,end_id)
                #print(rc.stress[predeccessor])
                successor=end_id
                while rc.od_id[successor]!=start_od_id:
                    rc.stress[predeccessor][successor]+=rc.motion_exchange[start_od_id][end_od_id]*fraction
                    predeccessor,successor=rc.distance[start_od_id][predeccessor][0],predeccessor
                    

        stress_to_store=[]
        for i,s in enumerate(rc.stress):
            for e in rc.stress[i]:
                stress_to_store.append({"start_id":i,"end_id":e,"stress":rc.stress[i][e]})
        self.do('stress/delete_stress')
        self.transaction('stress/import_stress',stress_to_store)

    @init_kwargs_as_parameters
    def stress_weight_connections(self,
            stress_name="stress",
            throughput_name="throughput",
            weight_name="weight",**kwargs):
        self.do('stress/create_weight_stress_change')
        self.do('stress/initialize_weight_stress_change',{
            "stress_name":stress_name,
            "throughput_name":throughput_name,
            "weight_name":weight_name
        })
        self.do('route/create_connection')
        self.do('stress/create_stressed_connection')

        



