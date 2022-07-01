-- checks if there are duble lines between start / end pint 
--


WITH
connections(start,end,count) as (
SELECT
  network_geometry.start,
  network_geometry.end,
  (
    SELECT
      count(*)
    FROM
      network_geometry as g1
    WHERE
      g1.start = network_geometry.start and
      g1.end = network_geometry.end
  ) as noofconnections
FROM
  network_geometry
)
SELECT
  *
FROM
  connections
WHERE
  connections.count>1
