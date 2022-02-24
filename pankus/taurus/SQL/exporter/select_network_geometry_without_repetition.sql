--
WITH
connections(start,end,linestring,count) as (
SELECT
  network_geometry.start,
  network_geometry.end,
  network_geometry.linestring,
  (
    SELECT
      count(*)
    FROM
      network_geometry as g1
    WHERE
      g1.start = network_geometry.start and
      g1.end = network_geometry.end
  ) as count
FROM
  network_geometry
)
SELECT
  *
FROM
  connections
WHERE
  connections.count=1
