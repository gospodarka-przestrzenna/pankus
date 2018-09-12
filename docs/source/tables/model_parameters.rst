model_parameters
=====================

Model_parameters table contains data on parameters of origin/destination points, including: origin-destination ID of a point, number of origins, number of destinations, selectivity value and convolution parameters

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   od_id,INT,ID number of computation area
   origins,REAL,Number of origins with destination in given origin-destination point
   destinations,REAL,Numbers of destinations with origin in given origin-destination point
   selectivity,REAL,"Parameter describing probability of object choosing a point as a destination, taking into consideration other points placed between the object and considered point"
   convolution_start,REAL,Number of destinations up to which model is computed classically
   convolution_size,REAL,Scope of destinations affected by convolution
   convolution_intensity,REAL,"Intensity of convolution, where 0 means there is no convolution and 1 means there is an absolute convolution. Values in between mean there is linear combination of two forms"
