INSERT INTO bmst_connection
SELECT DISTINCT
    start.id,
    end.id,
    network.weight
FROM
    network,
    point as start,
    point as end
WHERE
    network.start=start.point AND
    network.end=end.point;