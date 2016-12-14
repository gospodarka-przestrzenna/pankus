DELETE FROM sd_properties WHERE name=:name;
INSERT INTO sd_properties
    SELECT
        sd_id,
        :new_name,
        ""
    FROM
        (SELECT DISTINCT sd_id from sd_properties)


