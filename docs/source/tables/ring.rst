.. _ring_table:

ring
=====

Ring table contains data on placement of the destinations (meant as number of origin/destination computation areas) relative to origin

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_start_id,INT,ID number of the origin/destination point meant as origin ex.: for intervening opportunities penetration
   od_end_id,INT,ID number of the origin/destination point meant as destination ex.: for intervening opportunities penetration
   ring,INT,number of ring placement of destination in relation to origin
