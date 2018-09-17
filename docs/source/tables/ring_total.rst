ring_total
===========

Ring_total table contains data on id of origin-destination computation area which the rings are built from, number of ring, sum of destinations in this ring and sum of destinations from all of the previous rings

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_start_id,INT,ID number or computation area from which the ring are built
   ring,INT,number of ring
   destinations_in,REAL,sum of destinations in given ring
   destinations_prior,REAL,sum of destinations in previous rings
