--'clean_value.sql' deletes rows with property specified in python script from 'sd_properties'

DELETE FROM sd_properties WHERE name=:name;
INSERT INTO sd_properties
    SELECT
        sd_id,
        :new_name,
        ""
    FROM
        (SELECT DISTINCT sd_id from sd_properties)
