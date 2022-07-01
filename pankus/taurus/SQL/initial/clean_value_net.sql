--'clean_value_net.sql' deletes rows with property specified in python script from 'network_properties'

DELETE FROM network_properties WHERE name=:name;
INSERT INTO network_properties
    SELECT
        start,
        end,
        :new_name,
        :default
    FROM
        (SELECT DISTINCT start,end from network_properties)
