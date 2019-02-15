.. _motion_exchange_table:

motion_exchange
=========================

Motion_exchange table contains data on motion_exchange results meant as sum of objects transported from one computation area (origin/start) to another (destination/end)

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_start_id,INT,ID number of computation area meant as origin of motion exchange
   od_end_id,INT,ID number of computation area meant as destination of motion exchange
   motion_exchange,REAL,sum of origins transported to the destination area
