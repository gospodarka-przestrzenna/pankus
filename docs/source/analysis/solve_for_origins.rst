solve_for_origins
=================

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/point
  ../tables/motion_exchange_fraction
  ../tables/model_parameters


Effect
------ 
- Let's assume we have well stated destinations in :ref:`model_parameters_table` table. We may think about destinations as a sum of trips that arrives to origin-destination point from origins. The trips might be described by a motion exchange matrix. We end up with following equation: $A*O=D$ where A is motion exchange matrix; O is origins vector; D is destination vector; Vectors decribes state in each origin destination point. The described function solves equation $O=A\D$. This gives origins amounts that meet specified destination considering motion exchange matrix.
- :ref:`model_parameters_table` table is updated with new origins values
