build_rings_from_layout
=======================

.. autoclass:: taurus.InterveningOpportunities
    :members: build_rings_from_layout

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/ring_layout
  ../tables/ring
  ../tables/point
  ../tables/distance


Effect
------
- The `ring` table is created and writen with ring number for each origin/destinatin pair.
  The ring number is determined from each pair distance.
  The data in the `ring_layout` table creates distance intervals that are used to compute the ring number of the destination area according to the ring's origin.
