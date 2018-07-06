-- fix geometry
-- get points and bind to group of points
--

DROP TABLE IF EXISTS coordinated_point;
CREATE TABLE coordinated_point (
    x FLOAT,
    y FLOAT,
    point TEXT
);

CREATE INDEX IF NOT EXISTS coordinated_point_point_idx ON coordinated_point (point);

INSERT INTO coordinated_point (x,y,point)
SELECT
  cast(substr(trimed,1,pos-2) as real) as x ,cast(substr(trimed,pos+1) as real) as y ,point
FROM(
  SELECT
    point,trim(point,"[] ") as trimed ,instr(point,', ') AS pos
  FROM (
    SELECT
      point
    FROM
      sd_geometry
    UNION ALL
    SELECT
      start
    FROM
      network_geometry
    UNION ALL
    SELECT
      end
    FROM
      network_geometry
  )
);
--
-- SELECT DISTINCT
--   pf1.point,pf2.point
-- FROM
--   coordinated_point as pf1,
--   coordinated_point as pf2
-- WHERE
--   pf1.point != pf2.point AND
--   abs(pf1.x - pf2.x) < 2048 AND
--   abs(pf1.y - pf2.y) < 2048
-- ;

DROP TABLE IF EXISTS point_group;
CREATE TABLE point_group (
    point_representative TEXT,
    point TEXT
);

WITH RECURSIVE
  point_groupper(point_ref,point,x,y) AS (
  SELECT
    point,point,x,y
  FROM
    coordinated_point
  UNION
  SELECT
    pf1.point_ref,pf2.point,pf2.x,pf2.y
  FROM
    point_groupper as pf1,
    coordinated_point as pf2
  WHERE
   pf1.point != pf2.point AND
   pf1.point_ref < pf2.point AND
   abs(pf1.x - pf2.x) < :range AND
   abs(pf1.y - pf2.y) < :range
   )
INSERT INTO point_group (point_representative,point)
SELECT
  min(point_ref),point
FROM
  point_groupper
GROUP BY
  point;

UPDATE
  point_group
SET point_representative = (
  SELECT
    '[' || cast(cast(x*256 as int)/256.0 as text) || ', ' || cast(cast(y*256 as int)/256.0  as text) || ']'
  FROM
    ( SELECT
      x,y
    FROM
      coordinated_point
    WHERE
      coordinated_point.point = point_group.point_representative
    )
  LIMIT 1
);

UPDATE sd_geometry
SET point = (
  SELECT
    point_representative
  FROM
    point_group as pg
  WHERE
    pg.point = sd_geometry.point
);

UPDATE network_geometry
SET start = (
  SELECT
    point_representative
  FROM
    point_group as pg
  WHERE
    pg.point = network_geometry.start
);

UPDATE network_geometry
SET end = (
  SELECT
    point_representative
  FROM
    point_group as pg
  WHERE
    pg.point = network_geometry.end
);

UPDATE network_properties
SET start = (
  SELECT
    point_representative
  FROM
    point_group as pg
  WHERE
    pg.point = network_properties.start
);

UPDATE network_properties
SET end = (
  SELECT
    point_representative
  FROM
    point_group as pg
  WHERE
    pg.point = network_properties.end
);


DROP TABLE IF EXISTS coordinated_point;
DROP TABLE IF EXISTS point_group;
