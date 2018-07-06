INSERT INTO sd_properties
    SELECT
        sd_id,
        :sources_new_name,
        sources
    FROM
        model_parameters;

INSERT INTO sd_properties
    SELECT
        sd_id,
        :destinations_new_name,
        destinations
    FROM
        model_parameters;

INSERT INTO sd_properties
    SELECT
        sd_id,
        :selectivity_new_name,
        selectivity
    FROM
        model_parameters;

