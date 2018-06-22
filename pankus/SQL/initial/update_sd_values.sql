--'update_sd_values.sql' updates values of source-destination points' properties in 'sd_properties' table

UPDATE sd_properties
SET value=:value
WHERE
    sd_id=:sd_id AND
    name=:name
