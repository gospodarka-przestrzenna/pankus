destination_shift
==================
.. autoclass:: taurus.InterveningOpportunities
    :members: destinations_shift

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/model_parameters
  ../tables/motion_exchange


Effect
------
- ``model_parameters`` table is updated.
- Each origin/destination computation area's destinations are set to be the sum of arriving motions (from motion exchange) normalized to keep the total sum of initial destinations unchanged.
