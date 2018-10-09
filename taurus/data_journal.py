#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from .sqlite_database import SQLiteDatabase
import pkg_resources

class DataJournal(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs
        if self.table_exists('model_log'):
            pass
            #odzyskiwanie current_action_id
        else:
            self.do('datajournal/create_model_log')
        #self.current_action_uid=self.get_action_uid()
        self.parent_action_uid=kwargs.get('parent_action_uid',None)

    @staticmethod
    def logged_function(function):
        def wrapper(self,*args,**kwargs):
            parameter_list=[str(argg) for argg in args[1:]]
            parameter_list.extend([str(key)+'='+str(kwargs[key]) for key in list(kwargs.keys())])
            action=str(function.__name__)+"("+", ".join(parameter_list)+")"
            version=str(pkg_resources.require("pankus")[0].version)
            action_uid=self.get_action_uid()
            out=function(self,*args, **kwargs)
            self.do('datajournal/insert_model_log',{
                                                'action_uid':action_uid,
                                                'action':action,
                                                'p_action_uid':self.parent_action_uid,
                                                'version':version})
            self.parent_action_uid=action_uid
            return out
        return wrapper

    def get_action_uid(self):
        return self.one('datajournal/get_next_action_uid')[0]
