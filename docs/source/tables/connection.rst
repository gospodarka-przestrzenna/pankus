connection
==========

Table contains data on connections between specified locations in the network. Connections are used to create distances between locations in the network

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   start_id,INT,ID number of connection starting point
   end_id,INT,ID number of connection ending point
   weight,REAL,weight of described connection e.g. its capacity
