create_escape_fraction_selectivity
==================================

.. autoclass:: taurus.InterveningOpportunities
    :members: create_escape_fraction_selectivity

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/model_parameters


Effect
------
- model_parameters
  every selectivity field is set to newly calculated value.
  new parameter "selectivity", calculated by create_escape_fraction_selectivity function, is added to the model_parameters table using update_model_parameters.sql,
