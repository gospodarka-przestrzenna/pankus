.. _temp_motion_exchange_fraction_total_table:

temp_motion_exchange_fraction_total
===================================

.. warning:: 
   this is a system table, not meant to be used by a standard user

Temp_motion_exchange_fraction_total helper table contains data on motion_exchange results meant as total fraction of objects transported from one computation area (origin/start) to another (destination/end)

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_start_id,INT,ID number of computation area meant as origin of motion exchange
   total,FLOAT,sum of fractions of origins transported during motion_exchange
