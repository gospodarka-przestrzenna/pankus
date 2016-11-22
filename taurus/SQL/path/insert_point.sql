DELETE FROM point;
INSERT INTO point (point,sd_id)
    SELECT
        network.start AS point,
        sd.sd_id AS sd_id
    FROM
        network LEFT OUTER JOIN
        sd ON network.start=sd.point
    UNION
    SELECT
        network.end AS point,
        sd.sd_id AS sd_id
    FROM
        network LEFT OUTER JOIN sd ON network.end=sd.point;

UPDATE point SET id=(id-1);