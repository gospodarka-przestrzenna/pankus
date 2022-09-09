DELETE FROM cost_load_change;
INSERT INTO cost_load_change
    SELECT
        start.id,
        end.id,
        (SELECT
            value
         FROM
            network_properties
         WHERE
            network_properties.name = :load_name AND
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
            network_properties.name = :cost_name AND
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
