INSERT INTO distance
SELECT
    start_id,
    end_id,
    predecessor_id,
    successor_id,
    weight
FROM
    distance_ring
WHERE
    start_id={start_id} AND
    end_id={end_id} AND
    weight={weight};

INSERT INTO used VALUES(
    end_id
);

INSERT INTO distance_ring
SELECT DISTINCT
    d.start_id,
    c.end_id,
    c.start_id,
    d.successor_id,
    d.weight+c.weight
FROM
    distance_ring as d,
    connection as c
WHERE
    d.end_id={end_id} AND
    d.start_id={start_id} AND
    c.start_id=d.end_id AND
    NOT EXISTS (
        SELECT
            id
        FROM
            used
        WHERE
            id =c.end_id
        LIMIT 1
    );

DELETE FROM distance_ring
WHERE start_id={start_id} AND end_id={end_id};