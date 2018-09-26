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
- Each origin/destination point's destinations are set to be the sum of objects transported to this point during motion exchange divided by ratio of sum of destinations to sum of origins in the model.
