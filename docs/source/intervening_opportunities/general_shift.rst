general_shift
==============

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/model_parameters
  ../tables/motion_exchange


Effect
------
- :ref:`model_parameters_table` table is updated.
- Origins in each origin/destination point are set to be the sum of motions (from :ref:`motion_exchange_table`) arriving to this point.
- Destinations in each origin/destination point are set to be the sum of motions (from :ref:`motion_exchange_table`) arriving to this point.
