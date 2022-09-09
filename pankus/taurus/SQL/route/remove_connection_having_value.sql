--'insert_connection.sql' writes 'connection' table by selecting pairs of points' id from 'network_geometry' table and cost of the connection from 'network_parameters' table


DELETE FROM connection WHERE
EXISTS
(SELECT
    *
FROM
    point as start,
    point as end,
    network_properties
WHERE
    connection.start_id=start.id AND
    connection.end_id=end.id AND
    network_properties.start = start.point AND
    network_properties.end = end.point AND
    network_properties.name = :key AND
    network_properties.value = :value    
);