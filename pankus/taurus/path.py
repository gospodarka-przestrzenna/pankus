#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from .data_journal import DataJournal
from .utils import TaurusLongTask
from .utils import init_kwargs_as_parameters


class Path:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @init_kwargs_as_parameters
    @DataJournal.log_and_stash("path")
    def create_path(self,k_path=1,type="SQL",**kwargs):

        assert self.table_exists('distance')
        self.do('path/create_path')

        if k_path > 1:
            raise NotImplemented
        else:
            if type=="python":
                points=[(point,id,od_idi) for (point,id,od_idi) in self.do('path/select_point')]
                            
                max_point=max([p[1] for p in points])+1
                max_od_point=max([p[2] for p in points if p[2]])+1

                distance=[[None for i in range(max_point)] for j in range(max_od_point)]
                od_id=[None for i in range(max_point)]
                
                for p in points:
                    od_id[p[1]]=p[2]
                
                for start_id,end_id,predecessor_id,successor_id,weight in self.do('path/select_routes'):
                    distance[od_id[start_id]][end_id]=[predecessor_id]

                featured_points=[p[2] for p in points if p!=None] ,\
                                
                for _,start_id,start_od_id in TaurusLongTask(\
                                points ,\
                                additional_text='Paths',\
                                **kwargs):
                    if start_od_id==None:
                        continue
                    paths=[] #start_id,end_id,segment_id,segment_start_id,segment_end_id

                    for _,end_id,_ in points:
                        d = distance[start_od_id][end_id]
                        if start_id==end_id or d[0]==None:
                            continue
                        segment={
                                "start_id": start_id,
                                "end_id": end_id,
                                "segment_id": 0,
                                "segment_start_id": d[0], 
                                "segment_end_id": end_id
                            }
                        paths.append(segment)
                        while d[0]!=start_id:
                            d=distance[start_od_id][d[0]]
                            
                            segment={
                                "start_id": start_id,
                                "end_id": end_id,
                                "segment_id": segment["segment_id"]+1,
                                "segment_start_id": d[0], 
                                "segment_end_id": segment["segment_start_id"]
                            }
                            paths.append(segment)

                    self.transaction('path/import_path',paths)


            elif type=="SQL":

                featured_points=self.do('route/select_od_point').fetchall()

                for _,start,_, in TaurusLongTask(\
                                featured_points,\
                                additional_text='Paths',\
                                **kwargs):
                	self.do('path/create_path_for_od_point',{'start':start})

