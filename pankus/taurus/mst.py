#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .data_journal import DataJournal

class MST(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @DataJournal.log_and_stash("bmst_connection", "bmst")
    def minimum_spanning_tree(self,connection_type="distances",**kwargs):
        """
        Creates minimium spanning tree with levels on which level/step each
        tree edge were added. The same information is gathered for graph nodes.

        Read more here [https://en.wikipedia.org/wiki/Borůvka%27s_algorithm]
        Can be created out of network connections as basic case or from distances
        computed earlier in process.

        The funcion writes computed info to network_properties table under ""
        Args:
            connection_type (string): can be "connection" or "distance"

        """
        valid_coonection_types_names=["connection","distance"]
        self.do('mst/create_boruvka_mst')
        if connection_type in valid_coonection_types_names:
            self.do('mst/bmst_connections_from_'+connection_type)
        else
            raise ValueError("only suported values are: "+", ".join(valid_coonection_types_names))
        self.do('mst/initialize_bmst')
        self.mst()
        self.do('mst/save_bmst_parameters_form_'+connection_type)

    @DataJournal.log_and_stash("bmst", "bmst_used_connection")
    def mst(self,**kwargs):
        #iterator=iter(ProgressBar(range(len(featured_points)**2)))
        while not self.one('mst/bmst_finish_condition')[0]:
            self.do('mst/bmst_step')

    @DataJournal.log_and_stash("od_properties")
    def save_bmst_parameters_to_od_properties(self,suffix='supernode',**kwargs):
        max_level=self.one('bmst/select_max_level')[0]
        for level in range(max_level+1):
            self.do('bmst/save_bmst_to_od',{
                'level':level,
                'supernode_level_name':'L'+str(level)+suffix
            })

    @DataJournal.log_and_stash("network_properties")
    def save_bmst_parameters_to_network(self,suffix='supernode',level="Level",**kwargs):
        self.do('bmst/save_network_level',{
            'level_name':level
        })
        max_level=self.one('bmst/select_max_level')[0]
        for level in range(max_level+1):
            self.do('bmst/save_bmst_supernode_to_network_end',{
                'level':level,
                'supernode_level_name':'L'+str(level)+suffix
            })
