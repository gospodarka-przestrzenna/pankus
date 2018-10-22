build_weighted_rings
====================

.. autoclass:: taurus.InterveningOpportunities
    :members: build_weighted_rings

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
- table ``ring`` is created and/or written, using tables ``distance`` and ``point``.
  Created rings are separated by fixed distance specified as weight in function parameters.
  Number of each ring is determined from distance between points and provided weight parameter.
