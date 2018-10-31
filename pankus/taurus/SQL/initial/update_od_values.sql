--'update_od_values.sql' updates values of origin-destination points' properties in 'od_properties' table

UPDATE od_properties
SET value=:value
WHERE
    od_id=:od_id AND
    name=:name
