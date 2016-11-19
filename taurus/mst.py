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
        self.mst()

    def minimum_spanning_tree_from_distance(self):
        self.do('mst/create_boruvka_mst')
        self.do('mst/bmst_connections_from_distance')
        self.do('mst/initialize_bmst')
        self.mst()

    def mst(self):
        #iterator=iter(ProgressBar(range(len(featured_points)**2)))
        while not self.one('mst/bmst_finish_condition')[0]:
            self.do('mst/bmst_step')
