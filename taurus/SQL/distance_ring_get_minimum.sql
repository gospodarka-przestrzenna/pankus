SELECT
    start_id,
    end_id,
    predecessor_id,
    successor_id,
    min(weight) as weight,
    oid
FROM
    distance_ring