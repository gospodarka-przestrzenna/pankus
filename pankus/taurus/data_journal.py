#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pankus import __version__, __authors__

from .sqlite_database import SQLiteDatabase
import pkg_resources
import sqlite3
import csv

class DataJournal(SQLiteDatabase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kwargs=kwargs

        self.do('datajournal/create_model_log') if not self.table_exists('model_log') else False
        self.do('datajournal/create_data_stash') if not self.table_exists('data_stash') else False
        #self.current_action_uid=self.get_action_uid()
        self.parent_action_uid=kwargs.get('parent_action_uid',None)

    @staticmethod
    def logged_function(function):
        def wrapper(self,*args,**kwargs):
            parameter_list=[str(argg) for argg in args[1:]]
            parameter_list.extend([str(key)+'='+str(kwargs[key]) for key in list(kwargs.keys())])
            action=str(function.__name__)+"("+", ".join(parameter_list)+")"
            version=__version__
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

    @staticmethod
    def data_stash(table_name):
        def data_deco(function):
            def wrapper(self,*args,**kwargs):
                out=function(self,*args, **kwargs)
                #print(table_name)
                assert ";" not in table_name
                assert len(table_name)<30
                cursor=self.db_connection.execute("SELECT * FROM "+table_name)
                names = [description[0] for description in cursor.description]
                header=','.join(names)
                data=[str(row)[1:-1] for row in cursor]
                csv=header+"\n"+"\n".join(data)
                #print(csv)
                #print(self.parent_action_uid)
                self.do('datajournal/insert_data_stash',{
                                                    'action_uid':self.parent_action_uid,
                                                    'table_name':table_name,
                                                    'csv':csv})
                return out
            return wrapper
        return data_deco

    @staticmethod
    def log_and_stash(*args_general):
        def real_decorator(function):
            def wrapper(self,*args,**kwargs):
                function2=DataJournal.logged_function(function)
                for arg in args_general:
                    function2=(DataJournal.data_stash(arg))(function2)
                return function2(self,*args,**kwargs)
            return wrapper
        return real_decorator

