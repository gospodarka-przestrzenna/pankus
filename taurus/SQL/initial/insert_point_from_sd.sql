--'insert_point_from_sd.sql' selects coordinates and id of a source-destination point from 'sd_geometry' table and writes it in the 'point' table

DELETE FROM point;
INSERT INTO point (point,sd_id)
    SELECT
        sd_geometry.point AS point,
        sd_geometry.sd_id AS sd_id
    FROM
        sd_geometry;

UPDATE point SET id=(oid-1);
