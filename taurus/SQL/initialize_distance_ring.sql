DELETE FROM distance_ring;
INSERT INTO distance_ring
    SELECT
        connection.start_id,
        connection.end_id,
        connection.start_id,
        connection.end_id,
        connection.weight
    FROM
        connection
    WHERE
        connection.start_id={id};

INSERT INTO used VALUES(
    {id}
);

INSERT INTO distance VALUES (
    {id},
    {id},
    {id},
    {id},
    0
);