#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json,pdb
from .data_journal import DataJournal
from heapq import heappush,heappop

class MST(DataJournal):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @DataJournal.log_and_stash("bmst_connection", "bmst")
    def minimum_spanning_tree_from_network(self,**kwargs):
        self.do('mst/create_boruvka_mst')
        self.do('mst/bmst_connections_from_network')
        self.do('mst/initialize_bmst')
        self.save_bmst_parameters=self.save_bmst_parameters_to_od_properties
        self.mst()

    @DataJournal.log_and_stash("bmst_connection", "bmst")
    def minimum_spanning_tree_from_distance(self,**kwargs):
        self.do('mst/create_boruvka_mst')
        self.do('mst/bmst_connections_from_distance')
        self.do('mst/initialize_bmst')
        self.save_bmst_parameters=self.save_bmst_parameters_to_network
        self.mst()

    @DataJournal.log_and_stash()
    def save_bmst_parameters(self,suffix,**kwargs):
        #only proxy function Wont work until mst executed
        pass

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

    # @DataJournal.log_and_stash("bmst", "bmst_used_connection")
    # def mst(self,**kwargs):
    #     #iterator=iter(ProgressBar(range(len(featured_points)**2)))
    #     while not self.one('mst/bmst_finish_condition')[0]:
    #         self.do('mst/bmst_step')

    def mst(self,**kwargs):
        # provisional index is list that descibes real node number on each provisional posion [real_idx,rea_idx]
        provisional_idx=[]
        # start indexed dicts of
        connections=[]


        # INIT stage

        # for each connection
        for start_id,end_id,weight in  self.do('mst/select_bmst_connection'):
            # create provisioanl indxes
            try:
                provisional_start_id=provisional_idx.index(start_id)
            except IndexError:
                provisional_start_id=len(provisional_idx)
                provisional_idx.append(start_id)

            try:
                provisional_end_id=provisional_idx.index(end_id)
            except IndexError:
                provisional_end_id=len(provisional_idx)
                provisional_idx.append(end_id)

            connections.append((weight, (provisional_start_id,provisional_end_id)))


        # supernode (data for supernode that point is in) (node indexed list) [sn,sn,...]
        # supernode[node_id] returns supernode node_id is in
        # this data can be stored
        supernode=list(range(len(provisional_idx)))

        # nodes_in_supernode (data for nodes for supernode) (supernode indexed dictionary of list of nodes) {sn:[n,n,n..],sn:[n,n,n,...]}
        # nodes_in_supernode[supernode_id] returns list of node_is that are in bmst_bmst_supernode_idx
        nodes_in_supernode={a:[a] for a in supernode}
