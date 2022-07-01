DELETE FROM weight_stress_change;
INSERT INTO weight_stress_change
    SELECT
        start.id,
        end.id,
        (SELECT
            value
         FROM
            network_properties
         WHERE
            network_properties.name = :stress_name AND
            network_properties.start = start.point AND
            network_properties.end = end.point
         LIMIT 1
        ),
        (SELECT
            value
         FROM
            network_properties
         WHERE
            network_properties.name = :throughput_name AND
            network_properties.start = start.point AND
            network_properties.end = end.point
         LIMIT 1
        ),
        (SELECT
            value
         FROM
            network_properties
         WHERE
            network_properties.name = :weight_name AND
            network_properties.start = start.point AND
            network_properties.end = end.point
         LIMIT 1
        )
    FROM
        network_geometry,
        point as start,
        point as end
    WHERE
        network_geometry.start=start.point AND
        network_geometry.end=end.point;
