distance
========

Data used
----------

.. toctree::
   :maxdepth: 1
   :caption: Tables:

   ../tables/distance
   ../tables/point
   ../tables/connection


Effect
------
- :doc:`distance table<../tables/distance>` is created and/or written with distances combined from connections
- Distances are generated using Dijkstra algorithm, meaning the shortest path is found (see: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- For every origin/destination point distances to all the other points are generated
