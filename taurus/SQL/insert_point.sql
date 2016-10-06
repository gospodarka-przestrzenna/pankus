DELETE FROM point;
INSERT INTO point
    SELECT DISTINCT * FROM (
        SELECT
            network.start AS point,
            NULL,
            sd.sd_id AS sd_id
        FROM
            network LEFT OUTER JOIN
            sd ON network.start=sd.point
        UNION
        SELECT
            network.end AS point,
            NULL,
            sd.sd_id AS sd_id
        FROM
            network LEFT OUTER JOIN sd ON network.end=sd.point
    );
UPDATE point SET id=rowid;