--'select_for_motion_exchange.sql' prepares data from 'ring', 'ring_total' and 'model_parameters' tables to be used in 'motion_exchange' function from python script

SELECT
    r.sd_start_id,
    r.sd_end_id,
    r.ring,
    rt.destinations_in,
    rt.destinations_prior,
    mps.sources,
    mp.destinations,
    mp.selectivity,
    mp.convolution_start,
    mp.convolution_size,
    mp.convolution_intensity
FROM
    ring as r,
    ring_total as rt,
    model_parameters as mp,
    model_parameters as mps
WHERE
    r.ring=rt.ring AND
    r.sd_start_id=rt.sd_start_id AND
    r.sd_end_id=mp.sd_id AND
    r.sd_start_id=mps.sd_id
