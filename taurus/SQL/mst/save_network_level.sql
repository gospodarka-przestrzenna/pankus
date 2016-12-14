INSERT INTO network_properties
    SELECT
        start.point,
        end.point
        :level_name,
        level
    FROM
        bmst_used_connection,
        point as start,
        point as end
    WHERE
        bmst_used_connection.start=start.id AND
        bmst_used_connection.end=end.id;