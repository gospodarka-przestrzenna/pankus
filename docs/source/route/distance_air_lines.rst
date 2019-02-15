distance_air_lines
==================

.. :noindex: autoclass:: pankus.taurus.Route
    :members: distance_air_lines

Data used
----------

.. toctree::
   :maxdepth: 1
   :caption: Tables:

   ../tables/distance
   ../tables/point


Effect
------
- :doc:`distance table<../tables/distance>` is created and/or written with airline distances either with geometrical distance (if distance_type "geom" is chosen as keyword function argument) or with WGS 84 distance from vincenty algorithm (if distance_type "vincenty" is chosen as keyword function argument)
- distances created with `distance_air_lines` using vincenty algorithm are relative to motion across geoid

