#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .sqlite_database import SQLiteDatabase

class MST(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def minimum_spanning_tree_from_network(self):
        self.do('mst/create_boruvka_mst')
        self.do('mst/bmst_connections_from_network')
        self.do('mst/initialize_bmst')
        self.save_bmst_parameters=self.save_bmst_parameters_to_sd_properties
        self.mst()

    def minimum_spanning_tree_from_distance(self):
        self.do('mst/create_boruvka_mst')
        self.do('mst/bmst_connections_from_distance')
        self.do('mst/initialize_bmst')
        self.save_bmst_parameters=self.save_bmst_parameters_to_network
        self.mst()

    def save_bmst_parameters(self,suffix):
        #only proxy function Wont work until mst executed
        pass

    def save_bmst_parameters_to_sd_properties(self,suffix='supernode'):
        max_level=self.one('bmst/select_max_level')[0]
        for level in range(max_level+1):
            self.do('bmst/save_bmst_to_sd',{
                'level':level,
                'supernode_level_name':'L'+str(level)+suffix
            })

    def save_bmst_parameters_to_network(self,suffix='supernode',level="Level"):
        self.do('bmst/save_network_level',{
            'level_name':level
        })
        max_level=self.one('bmst/select_max_level')[0]
        for level in range(max_level+1):
            self.do('bmst/save_bmst_supernode_to_network_end',{
                'level':level,
                'supernode_level_name':'L'+str(level)+suffix
            })





    def mst(self):
        #iterator=iter(ProgressBar(range(len(featured_points)**2)))
        while not self.one('mst/bmst_finish_condition')[0]:
            self.do('mst/bmst_step')
