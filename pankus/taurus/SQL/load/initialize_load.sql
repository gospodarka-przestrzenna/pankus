--just zeroed stress table

DELETE FROM stress;
INSERT INTO stress
    SELECT
        start.id,
        end.id,
        IFNULL((SELECT
				value
			FROM
				network_properties
			WHERE
				network_properties.name = :stress_name AND
				network_properties.start = start.point AND
				network_properties.end = end.point
			LIMIT 1
			),0)
    FROM
        network_geometry,
        point as start,
        point as end
    WHERE
        network_geometry.start=start.point AND
        network_geometry.end=end.point;
