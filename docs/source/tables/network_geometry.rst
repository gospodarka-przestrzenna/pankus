network_geometry
================

Network_geometry table contains data on start and end of a segment of the network and

.. csv-table::
   :widths: 2,1,9
   :header-rows: 1

   Field name,Field type,Description
   start,TEXT,geometry (in fixed format) of segment starting point
   end,TEXT,geometry (in fixed format) of segment ending point
   linestring,TEXT,geometries (in fixed format) of road between two junctions

By geometry in fixed format we understand anything that is well understandable string.
This might be python tuple or list with coordinates
e.g.: string like ``[1.45, 14.89]`` clearly denotes point.


Same with linestring geometry ``[[x1, y1], [x2, y2], [x3, y3]]`` clearly descries line with two segments between 3 points

..  warning::
    for now only the geometry in form of python tuples is supported
