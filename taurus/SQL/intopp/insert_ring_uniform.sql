--'insert_ring_uniform.sql' writes 'ring' table using 'point' and 'distance' tables. Script 'insert_ring_uniform.sql' selects pairs of source-destinations points from 'point' table and matches them with corresponding ring, expressed as value of weight of distance between points multiplied by a factor calculated in the 'buid_uniform_rings' fuction in the 'intervening_opportunity' script

INSERT INTO ring
SELECT DISTINCT
    p1.sd_id,
    p2.sd_id,
    (SELECT
        cast(weight*(:factor) as int)
    FROM
        distance as d
    WHERE
        d.start_id=p1.id AND
        d.end_id=p2.id
    LIMIT 1)
FROM
    point as p1,
    point as p2
WHERE
    p1.sd_id NOT NULL AND
    p2.sd_id NOT NULL;
