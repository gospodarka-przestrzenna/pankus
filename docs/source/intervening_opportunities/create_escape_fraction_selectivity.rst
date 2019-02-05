create_escape_fraction_selectivity
==================================

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/model_parameters


Effect
------
- function changes selectivity in ``model_parameters`` table. Every selectivity field is set to newly calculated value. New "selectivity" parameter is calculated so that total escapes from simulation area value is a fraction of total origins provided as a parameter.
