.. _model_log_table:

model_log
==========

Model_log table serves as a documentation of a simulation process and contains data on executed functions such as names of the functions, their parameters, time of execution and version of pankus used to run simulation

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   action_uid,INT,ID number of an action meant as executed function with specific parameters
   action,TEXT,function name combined with set of its parameters
   datetime,TEXT,time of function execution in epoch
   p_action_uid,TEXT,ID number of previous ("parent") action
   version,TEXT,pankus version the function is originating froms
