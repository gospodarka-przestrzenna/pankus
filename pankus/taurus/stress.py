#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb,math
from .utils import TaurusLongTask
from .data_journal import DataJournal
from .utils import init_kwargs_as_parameters

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

    def initialize_stress(self,weight="weight",**kwargs):
        """ 
            Creates stress table, that holds stress for a graph.
        """
        self.do('stress/create_stress')

    def do_stress(self,type="progressbar",**kwargs):
        """
        """
        assert self.table_exists('motion_exchange')
        assert self.table_exists('path')
        assert self.table_exists('stress')
        
        if type=='progressbar':

            points=[(point,id,od_idi) for (point,id,od_idi) in self.do('stress/select_point')]
                        
            max_point=max([p[1] for p in points])+1
            max_od_point=max([p[2] for p in points if p[2]])+1

            motion_exchange=[[None for i in range(max_od_point)] for j in range(max_od_point)]
            od_id=[None for i in range(max_point)]
            stress=[{} for i in range(max_point)]

            for p in points:
                od_id[p[1]]=p[2]
            
            for start,end,value in self.do('stress/select_motion_exchange'):
                motion_exchange[start][end]=value

            expected_problem_size,=self.do('stress/select_path_count').fetchone()

            for start,end,_,sstart,send in TaurusLongTask(\
                                            self.do('stress/select_path'),\
                                            max_value=expected_problem_size,\
                                            additional_text='Stressing',\
                                            **kwargs):
                if od_id[end]:
                    if send not in stress[sstart]:
                        stress[sstart][send]=motion_exchange[od_id[start]][od_id[end]]
                    else:
                        stress[sstart][send]+=motion_exchange[od_id[start]][od_id[end]]

            stress_to_store=[]
            for i,s in enumerate(stress):
                for e in stress[i]:
                    stress_to_store.append({"start_id":i,"end_id":e,"stress":stress[i][e]})
            self.transaction('stress/import_stress',stress_to_store)

        elif type=="SQL":
            self.do('stress/stress_connections')

    def save_stress(self,saved_name='stress',**kwargs):
        """
        Saves stress to network_parameters
        """
        self.do('initial/clean_value_net',{'name':saved_name,"new_name":saved_name,"default":"0"})
        self.do('stress/save_stress_to_net',{'name':saved_name})



