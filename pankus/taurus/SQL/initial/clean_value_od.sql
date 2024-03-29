--'clean_value_od.sql' deletes rows with property specified in python script from 'od_properties'

DELETE FROM od_properties WHERE name=:name;
INSERT INTO od_properties
    SELECT
        od_id,
        :new_name,
        :default
    FROM
        (SELECT DISTINCT od_id from od_properties)
