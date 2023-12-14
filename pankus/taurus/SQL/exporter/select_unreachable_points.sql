-- we will select the points that are unreachable from the given od_id point \
-- we check where the cost is infinit and the 

-- We want to select random od_id from the point table if :od_id is null
-- We want to select the od_id from the point table if :od_id is not null



SELECT
    p_end.id,
    p_end.point
FROM
    (
     SELECT * FROM (SELECT id,od_id FROM point WHERE od_id == :od_id limit 1) as p1
     UNION ALL
     SELECT * FROM (SELECT id,od_id FROM point WHERE od_id is not NULL ORDER BY RANDOM() LIMIT 1) as p2
    ) as p,
    distance as d,
    point as p_end
WHERE

    d.start_id = p.id AND
    d.cost == 1e999 AND
    d.end_id = p_end.id