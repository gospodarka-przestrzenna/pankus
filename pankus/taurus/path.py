#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Wawrzyniec Zipser, Maciej Kamiński Politechnika Wrocławska'

from .data_journal import DataJournal
from .utils import TaurusLongTask
from .utils import init_kwargs_as_parameters
from .utils import RouteCache


class Path:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @init_kwargs_as_parameters
    @DataJournal.log_and_stash("path")
    def create_path(self,k_path=1,method="SQL",**kwargs):

        assert self.table_exists('distance')
        self.do('path/create_path')

        if k_path > 1:
            raise NotImplemented
        else:
            if method=="python":
                rc=RouteCache()
                rc.cache_distances()

                for _,start_id,start_od_id in TaurusLongTask(\
                                rc.points ,\
                                additional_text='Paths',\
                                **kwargs):
                    if start_od_id==None:
                        continue
                    paths=[] #start_id,end_id,segment_id,segment_start_id,segment_end_id

                    for _,end_id,_ in rc.points:
                        predeccessor = rc.distance[start_od_id][end_id][0]
                        if start_id==end_id or predeccessor==None:
                            continue
                        segment={
                                "start_id": start_id,
                                "end_id": end_id,
                                "segment_id": 0,
                                "segment_start_id": predeccessor, 
                                "segment_end_id": end_id
                            }
                        paths.append(segment)
                        while d[0]!=start_id:
                            predeccessor=rc.distance[start_od_id][predeccessor][0]
                            
                            segment={
                                "start_id": start_id,
                                "end_id": end_id,
                                "segment_id": segment["segment_id"]+1,
                                "segment_start_id": predeccessor, 
                                "segment_end_id": segment["segment_start_id"]
                            }
                            paths.append(segment)

                    self.transaction('path/import_path',paths)


            elif method=="SQL":

                featured_points=self.do('route/select_od_point').fetchall()

                for _,start,_, in TaurusLongTask(\
                                featured_points,\
                                additional_text='Paths',\
                                **kwargs):
                	self.do('path/create_path_for_od_point',{'start':start})

