build_rings_from_layout
=======================

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
- The :ref:`ring_table` table is created and written with ring number for each origin/destination pair.
  The ring number is determined from each pair distance.
  The data in the :ref:`ring_layout_table` table creates distance intervals that are used to compute the ring number of the destination area according to the ring's origin.
