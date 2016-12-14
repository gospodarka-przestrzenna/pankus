UPDATE sd_properties
SET value=:value
WHERE
    sd_id=:sd_id AND
    name=:name