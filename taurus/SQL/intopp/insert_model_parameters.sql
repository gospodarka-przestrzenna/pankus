--'insert_model_parameters.sql' writes 'model_parameters' table using 'sd_properties' and 'sd_geometry' tables

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
        CASE WHEN (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :convolution_intensity_name LIMIT 1) IS NULL
        THEN 0
        ELSE (select value from sd_properties
        where sd_geometry.sd_id=sd_id and name = :convolution_intensity_name LIMIT 1)
        END

    FROM
        sd_geometry;
