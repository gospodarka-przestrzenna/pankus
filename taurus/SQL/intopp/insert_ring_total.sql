--'insert_ring_total.sql' writes 'ring_total' table using 'ring' and 'model_parameters' tables, selecting from them id of a origin-destination point, number of ring which the point is placed in, number of destinations in this ring and sum of destination from prior rings

INSERT INTO ring_total
SELECT
    r.od_start_id,
    r.ring,
    sum(destinations),
    (SELECT
        CASE WHEN sum(destinations)
        IS NULL THEN 0
        ELSE sum(destinations)
        END
    FROM
        ring,
        model_parameters as odq
    WHERE
        od_start_id=r.od_start_id AND
        od_end_id=odq.od_id AND
        ring < r.ring)

FROM
    ring as r,
    model_parameters
WHERE
    od_end_id=od_id
GROUP BY
    r.od_start_id,
    r.ring;
