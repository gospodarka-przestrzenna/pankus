.. _data_stash_table:

data_stash
==========

Data_stash table contains data on tables content after a specific function execution, table content is written in csv format.

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   action_uid,INT,ID number of an action meant as executed function with specific parameters
   table_name,TEXT,name of a table
   csv,TEXT,content of the table in csv format
