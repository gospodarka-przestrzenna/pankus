distance
========

Distance table contains data on distances between locations or in particular between locations and each point in the network. Each distance is expressed as a set of connections

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   start_id,INT,ID number of path starting point
   end_id,INT,ID number of path ending point
   predecessor_id,INT,ID number of the point preceeding the ending point on the path
   successor_id,INT,ID number of the area following the starting point on the path
   weight,REAL,weight of described distance e.g. its capacity
