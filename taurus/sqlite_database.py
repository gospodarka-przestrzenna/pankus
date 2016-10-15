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
        database_name=kwargs.get('database_name','taurus.db')
        self.db_connection=sqlite3.connect(database_name)
        self.do_progressbar=kwargs.get('progressbar',True)

    def get_sql_form_file(self,script_name):
        return pkg_resources.resource_stream(__name__,'SQL/'+script_name+'.sql').read().decode('utf-8')

    def build_sql(self,script_string,args={}):
        return script_string.format(**args)

    def executemany(self,script_name,args_list):
        return self.db_connection.executemany(
            self.get_sql_form_file(script_name),
            args_list
        )
    def commit(self):
        self.db_connection.commit()

    def do(self,script_name,args=None):
        sql_string=self.get_sql_form_file(script_name)
        if not args:
            if ';' in sql_string:
                self.db_connection.executescript(sql_string)
            else:
                return self.db_connection.execute(sql_string)
        elif hasattr(args,'__iter__'):
            return self.db_connection.executemany(sql_string,args)
        elif isinstance(args,list):
            return self.db_connection.execute(sql_string,args)
        else:
            return self.db_connection.executescript(self.build_sql(sql_string,args))

    def table_exists(self,dataset_name):
        c=self.db_connection.cursor()
        return not c.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
            [dataset_name]).fetchone()[0]==0

    def _taurus_progressbar_cursor(self,script):
        if self.do_progressbar:
            return ProgressBar(self.do(script).fetchall())
        else:
            return self.do(script).fetchall()


