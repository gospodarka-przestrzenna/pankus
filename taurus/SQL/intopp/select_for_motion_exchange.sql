SELECT
    r.sd_start_id,
    r.sd_end_id,
    r.ring,
    rt.destinations_in,
    rt.destinations_prior,
    mp.sources,
    mp.destinations,
    mp.selectivity,
    mp.convolution_start,
    mp.convolution_size,
    mp.convolution_intensity
FROM
    ring as r,
    ring_total as rt,
    model_parameters as mp
WHERE
    r.ring=rt.ring AND
    r.sd_start_id=rt.sd_start_id AND
    r.sd_end_id=mp.sd_id