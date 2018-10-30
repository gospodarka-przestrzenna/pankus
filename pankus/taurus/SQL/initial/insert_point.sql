--'insert_point.sql' writes table 'point', 'network_geometry' and 'od_geometry' tables are used
-- od_id might be NULL if point from network doesn't exist in od_geometry
-- populates point table with junkctions points

DELETE FROM point;
INSERT INTO point (point,od_id)
    SELECT
        network_geometry.start AS point,
        od_geometry.od_id AS od_id
    FROM
        network_geometry LEFT OUTER JOIN
        od_geometry ON network_geometry.start=od_geometry.point
    UNION
    SELECT
        network_geometry.end AS point,
        od_geometry.od_id AS od_id
    FROM
        network_geometry LEFT OUTER JOIN
        od_geometry ON network_geometry.end=od_geometry.point;

UPDATE point SET id=(oid-1);
