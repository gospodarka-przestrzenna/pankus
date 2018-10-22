build_uniform_rings
====================

.. autoclass:: taurus.InterveningOpportunities
  :members: build_uniform_rings

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
- table ``ring`` is created and/or written, using tables ``distance`` and ``point``, with number of rings specified in function parameters.
  Created rings are separated by uniform distance, determined from maximum distance in model and given number of rings.
