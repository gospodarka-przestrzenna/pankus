--'insert_model_parameters.sql' writes 'model_parameters' table using 'od_properties' and 'od_geometry' tables

DELETE FROM model_parameters;
INSERT INTO model_parameters
    SELECT
        od_id,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :origins_name LIMIT 1),
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :destinations_name LIMIT 1),
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :selectivity_name LIMIT 1),
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :convolution_start_name LIMIT 1),
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :convolution_size_name LIMIT 1),
        CASE WHEN (select value from od_properties
        where od_geometry.od_id=od_id and name = :convolution_intensity_name LIMIT 1) IS NULL
        THEN 0
        ELSE (select value from od_properties
        where od_geometry.od_id=od_id and name = :convolution_intensity_name LIMIT 1)
        END

    FROM
        od_geometry;
