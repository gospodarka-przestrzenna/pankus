--
DELETE FROM ring
WHERE EXISTS(
    SELECT 
        *
    FROM
        point as p1,
        point as p2,
        distance as d
    WHERE
        ring.od_start_id=p1.od_id AND
        ring.od_end_id=p2.od_id AND
        d.start_id = p1.id AND
        d.end_id = p2.id AND
        d.weight > :critical_distance
)