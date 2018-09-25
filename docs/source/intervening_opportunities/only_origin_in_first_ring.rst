only_origin_in_first_ring
=========================
.. autoclass:: taurus.InterveningOpportunities
    :members: only_origin_in_first_ring

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
- Table ``ring`` is updated with new ring column values.
  If there exists not empty set containing current element with distance greater than 0, points are moved to the next ring.
