network_properties
==================

Network_properties table contains data on start and end of segments of the network, name of segment parameter and its value

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   start,TEXT,geometry (in fixed format) of segment starting point
   end,TEXT,geometry (in fixed format) of segment ending point
   name,TEXT,name of a parameter describing segment of the network
   value,TEXT,value of the parameter

By geometry in fixed format we understand anything that is well understandable string.
This might be python tuple or list with coordinates
e.g.: string like ``[1.45, 14.89]`` clearly denotes point.


Same with linestring geometry ``[[x1, y1], [x2, y2], [x3, y3]]`` clearly descries line with two segments between 3 points

..  warning::
    for now only the geometry in form of python tuples is supported
