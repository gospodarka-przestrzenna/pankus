-- shows od points that doesn't have coresponding/aligned network terminators
--

SELECT
  od_geometry.point
FROM
  od_geometry LEFT OUTER JOIN
  network_geometry ON network_geometry.start=od_geometry.point
WHERE
  network_geometry.start IS NULL
INTERSECT
SELECT
  od_geometry.point
FROM
  od_geometry LEFT OUTER JOIN
  network_geometry ON network_geometry.end=od_geometry.point
WHERE
  network_geometry.end IS NULL
