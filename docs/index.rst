.. pankus documentation master file, created by
   sphinx-quickstart on Fri Sep  7 22:16:10 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pankus's documentation!
==================================

.. warning::
   This documentstion is meant for oftware in active development

Pankus is meant as a collection of subpackages, under this name are available various spatial analyses libraries. Basic functionality of pankus package is meant to provide users with simple tools that might be combined into simulation models. 

You can find here glossary, explained functions and tables as well as use cases for project structures. 
Feel free to let us know if you think there is something missing ;)

Terms
-----
.. toctree::
   :maxdepth: 1
   :glob:

   source/terms/terms

Tables
------
.. toctree::
   :maxdepth: 1
   :glob:

   source/tables

Modules
-------
.. toctree::
   :maxdepth: 1
   :glob:

   source/modules/*

Examples of use
---------------

.. code-block:: python

   #creating instance of Taurus Class, enabling progressbar and setting database to be created in memory
   T = Taurus(progressbar=True, database_name=":memory:")
   #generating network in specific shape in specified by the user size
   T.make_hexdiagonal_pattern_network(problem_size)
   #generating connections between pairs of points in the network
   T.generate_connections()
   #generating distances built from connections
   T.distance()

.. code-block:: python

   #creating specified by the user number of interval rings for each origin point
   T.build_uniform_rings(rings)
   #importing parameters of a model
   T.import_model_parameters()
   #calculating sum of destinations in rings
   T.ring_total()
 


