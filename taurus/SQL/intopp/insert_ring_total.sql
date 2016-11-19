INSERT INTO ring_total
SELECT
    r.sd_start_id,
    r.ring,
    sum(destinations),
    (SELECT
        CASE WHEN sum(destinations)
        IS NULL THEN 0
        ELSE sum(destinations)
        END
    FROM
        ring,
        sd as sdq
    WHERE
        sd_start_id=r.sd_start_id AND
        sd_end_id=sdq.sd_id AND
        ring < r.ring)

FROM
    ring as r,
    sd
WHERE
    sd_end_id=sd_id
GROUP BY
    r.sd_start_id,
    r.ring;


