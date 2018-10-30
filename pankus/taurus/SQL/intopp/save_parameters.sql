INSERT INTO od_properties
    SELECT
        od_id,
        :origins_new_name,
        origins
    FROM
        model_parameters;

INSERT INTO od_properties
    SELECT
        od_id,
        :destinations_new_name,
        destinations
    FROM
        model_parameters;

INSERT INTO od_properties
    SELECT
        od_id,
        :selectivity_new_name,
        selectivity
    FROM
        model_parameters;
