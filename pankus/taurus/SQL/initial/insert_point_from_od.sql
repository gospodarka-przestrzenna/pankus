--'insert_point_from_od.sql' selects coordinates and id of a origin-destination point from 'od_geometry' table and writes it in the 'point' table

DELETE FROM point;
INSERT INTO point (point,od_id)
    SELECT
        od_geometry.point AS point,
        od_geometry.od_id AS od_id
    FROM
        od_geometry;

UPDATE point SET id=(oid-1);
