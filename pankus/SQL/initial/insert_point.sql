--'insert_point.sql' writes table 'point', 'network_geometry' and 'sd_geometry' tables are used
-- sd_id might be NULL if point from network doesn't exist in sd_geometry
-- populates point table with junkctions points 

DELETE FROM point;
INSERT INTO point (point,sd_id)
    SELECT
        network_geometry.start AS point,
        sd_geometry.sd_id AS sd_id
    FROM
        network_geometry LEFT OUTER JOIN
        sd_geometry ON network_geometry.start=sd_geometry.point
    UNION
    SELECT
        network_geometry.end AS point,
        sd_geometry.sd_id AS sd_id
    FROM
        network_geometry LEFT OUTER JOIN
        sd_geometry ON network_geometry.end=sd_geometry.point;

UPDATE point SET id=(oid-1);
