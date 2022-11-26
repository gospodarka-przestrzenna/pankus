--
SELECT
    rl.ring_number,
    rl.ring_size,
    rl.prior_rings_size
FROM
    ring_layout as rl,
    (select od_id from point where od_id is not NULL limit 1) as p
WHERE
    rl.od_id = p.od_id 
ORDER BY
    rl.ring_number