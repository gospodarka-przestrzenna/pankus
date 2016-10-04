#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import sqlite3
import pkg_resources

class SQLiteDatabase(object):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        database_name='taurus.db'#kwargs.get('database_name','taurus.db')
        self.db_connection=sqlite3.connect(database_name)

    def execute(self,SQL,args={}):
        with open(SQL,'r') as sqlfile:
            c=self.db_connection.cursor()
            c.execute(sqlfile.read(),args)
            self.db_connection.commit()
            return c

    def execute_script(self,script_name,args={}):
        c=self.db_connection.cursor()
        sql_string=pkg_resources.resource_stream(__name__,'SQL/'+script_name+'.sql').read().decode('utf-8')
        print(sql_string.format(**args))
        c.executescript(sql_string.format(**args))
        return c
