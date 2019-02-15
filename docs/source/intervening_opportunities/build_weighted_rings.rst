build_weighted_rings
====================

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/ring
  ../tables/distance
  ../tables/point


Effect
------
- table :ref:`ring_table` is created and/or written, using tables :ref:`distance_table` and :ref:`point_table`.
  Created rings are separated by fixed distance specified as weight in function parameters.
  Number of each ring is determined from distance between points and provided weight parameter.
