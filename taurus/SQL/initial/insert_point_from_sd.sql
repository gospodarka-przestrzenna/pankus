DELETE FROM point;
INSERT INTO point (point,sd_id)
    SELECT
        sd_geometry.point AS point,
        sd_geometry.sd_id AS sd_id
    FROM
        sd_geometry;

UPDATE point SET id=(oid-1);