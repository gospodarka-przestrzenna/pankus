DELETE FROM model_parameters;
INSERT INTO model_parameters
    SELECT
        sd_id,
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :sources_name LIMIT 1),
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :destinations_name LIMIT 1),
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :selectivity_name LIMIT 1),
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :convolution_start_name LIMIT 1),
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :convolution_size_name LIMIT 1),
        (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :convolution_intensity_name LIMIT 1)
    FROM
        sd_geometry;