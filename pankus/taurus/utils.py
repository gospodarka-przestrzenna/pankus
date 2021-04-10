#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import progressbar as pb
from functools import wraps

class TaurusLongTask:

    def __init__(self,iterable,
                    progressbar=True,
                    max_value=pb.UnknownLength,
                    additional_text='',
                    **kwargs):
        self.iterator=iter(iterable)
        self.if_progressbar=progressbar
        if hasattr(iterable, '__len__'):
            self.max_value=len(iterable)
        else:
            self.max_value=max_value
        self.additional_text=additional_text
        self.bar_widgets=[ \
                            additional_text+' [', pb.Timer(), '] ', \
                            pb.Bar(), \
                            ' (', pb.ETA(), ') ', \
                        ]

    def __iter__(self):
        if self.if_progressbar:
            self.bar=pb.ProgressBar(\
                max_value=self.max_value,\
                widgets=self.bar_widgets,\
            )
            return self
        return self.iterator

    def __next__(self):
        try:
            element = self.iterator.__next__()
            self.bar.update(self.bar.value+1)
            return element
        except Exception as error:
            self.bar.finish()
            raise error

def init_kwargs_as_parameters(function):
    @wraps(function)
    def wrapper(self,*args,**kwargs):
        return function(self,*args,**{**self.kwargs,**kwargs})
    return wrapper



class RouteCache:
    def __init__(self,taurus_object):
        self.taurus_object=taurus_object


        self.points=[(point,id,od_idi) for (point,id,od_idi) in self.taurus_object.do('path/select_point')]
                            
        self.max_point=max([p[1] for p in self.points])+1
        self.max_od_point=max([p[2] for p in self.points if p[2]])+1
        self.od_id=[None for i in range(self.max_point)]
        
        for p in self.points:
            self.od_id[p[1]]=p[2]
        
        self.featured_points=[p[2] for p in self.points if p[2]!=None]

    def cache_distances(self):
        assert self.taurus_object.table_exists('distance')
        self.distance=[[None for i in range(self.max_point)] for j in range(self.max_od_point)]

        for start_id,end_id,predecessor_id,successor_id,weight in self.taurus_object.do('path/select_routes'):
            self.distance[self.od_id[start_id]][end_id]=[predecessor_id,weight]

    def cache_motion_exchange(self):
        assert self.taurus_object.table_exists('motion_exchange')
        self.motion_exchange=[[None for i in range(self.max_od_point)] for j in range(self.max_od_point)]
        for start,end,value in self.taurus_object.do('stress/select_motion_exchange'):
            self.motion_exchange[start][end]=value

    def cache_stress(self):
            assert self.taurus_object.table_exists('stress')
            self.stress=[{} for i in range(self.max_point)]
            for start_id,end_id,stress in self.taurus_object.do('stress/select_stress'):
                self.stress[start_id][end_id]=stress



