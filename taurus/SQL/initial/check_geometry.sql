-- shows sd points that doesn't have coresponding/aligned network terminators
--

SELECT
  sd_geometry.point
FROM
  sd_geometry LEFT OUTER JOIN
  network_geometry ON network_geometry.start=sd_geometry.point
WHERE
  network_geometry.start IS NULL
INTERSECT
SELECT
  sd_geometry.point
FROM
  sd_geometry LEFT OUTER JOIN
  network_geometry ON network_geometry.end=sd_geometry.point
WHERE
  network_geometry.end IS NULL
