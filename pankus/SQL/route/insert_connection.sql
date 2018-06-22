--'insert_connection.sql' writes 'connection' table by selecting pairs of points' id from 'network_geometry' table and weight of the connection from 'network_parameters' table

DELETE FROM connection;
INSERT INTO connection
    SELECT
        start.id,
        end.id,
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
