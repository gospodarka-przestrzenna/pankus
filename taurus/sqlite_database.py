#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import sqlite3
import pkg_resources
from ipy_progressbar import ProgressBar

class SQLiteDatabase:

    def __init__(self,**kwargs):
        #super().__init__(**kwargs)
        self.kwargs=kwargs
        self.kwargs=kwargs
        database_name='taurus.db'#kwargs.get('database_name','taurus.db')
        self.db_connection=sqlite3.connect(database_name)

    def execute(self,sql,args=[]):
        c=self.db_connection.cursor()
        c.execute(sql,args)
        self.db_connection.commit()
        return c

    def execute_script(self,script_name,args={}):
        c=self.db_connection.cursor()
        sql_string=pkg_resources.resource_stream(__name__,'SQL/'+script_name+'.sql').read().decode('utf-8')
        sql_string=sql_string.format(**args)
        if self.kwargs.get('show_sql_query',False):
           print(sql_string)
        if ';' in sql_string:
            c.executescript(sql_string)
        else:
            c.execute(sql_string)
        return c


    def table_exists(self,dataset_name):
        c=self.db_connection.cursor()
        return not c.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
            [dataset_name]).fetchone()[0]==0


    def _taurus_progressbar_cursor(self,script):
        if self.kwargs.get('progressbar',True):
            # print(self.execute_script(script).fetchall())
            return ProgressBar(self.execute_script(script).fetchall())
        else:
            return self.execute_script(script).fetchall()
