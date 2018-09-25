normalize_motion_exchange
=========================
.. autoclass:: taurus.InterveningOpportunities
   :members: normalize_motion_exchange

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/motion_exchange_fraction
  ../tables/motion_exchange


Effect
------
- ``motion_exchange_fraction`` and ``motion_exchange`` table are updated with new, normalized values.
  After this total sum in tables ``motion_exchange_fraction`` and ``motion_exchange`` are equal to initial total mass or 1 respectively.
  These values are computed by multplying each of updated values by proper factor.
