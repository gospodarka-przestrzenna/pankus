data_stash
====================

Data used
----------

.. toctree::
  :maxdepth: 1
  :caption: Tables:

  ../tables/data_stash

Effect
------
- table ``data_stash`` is created and/or written with action id, name of a table and its content after action's execution in csv format 
- ``data_stash`` function is written as a wrapper to make documenting functions user friendly
- ``data_stash`` stores data after every executed function that may change SQL tables content
