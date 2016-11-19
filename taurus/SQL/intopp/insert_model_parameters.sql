DELETE FROM model_parameters;
INSERT INTO model_parameters
    SELECT
        sd_id,
        sources,
        destinations,
        selectivity,
        convolution_start,
        convolution_size,
        convolution_intensity
    FROM sd;