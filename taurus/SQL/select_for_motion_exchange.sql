SELECT
    r.sd_start_id,
    r.sd_end_id,
    r.ring,
    rt.destinations_in,
    rt.destinations_prior,
    sd.sources,
    sd.destinations,
    sd.selectivity
FROM
    ring as r,
    ring_total as rt,
    sd
WHERE
    r.ring=rt.ring AND
    r.sd_start_id=rt.sd_start_id AND
    r.sd_end_id=sd.sd_id