motion_exchange
==================
.. autoclass:: taurus.InterveningOpportunities
   :members: motion_exchange

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/motion_exchange
  ../tables/motion_exchange_fraction
  ../tables/ring
  ../tables/ring_total
  ../model_parameters


Effect
------
- ``motion_exchange_fraction`` and ``motion_exchange`` table are created and written.
- Fraction of motion exchange is set to be the the differential between fraction of "objects" that found destinations prior and in the currently chosen ring and fraction of all "objects" that found destinations prior to the currently chosen ring multiplied by destinations and divided by destinations in specific ring.
- Motion exchange is set to be the fraction of motion exchange multiplied by number of origins
