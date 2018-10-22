motion_exchange_fraction
=========================

Motion_exchange_fraction table contains data on motion_exchange results meant as fraction of objects transported from one computation area (origin/start) to another (destination/end)

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_start_id,INT,ID number of computation area meant as origin of motion exchange
   od_end_id,INT,ID number of computation area meant as destination of motion exchange
   fraction,REAL,fraction of objects transported from the origin area to the destination area
