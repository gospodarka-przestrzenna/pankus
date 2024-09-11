--'od_distance_maximum.sql' exports maximum distance from the table 'distance' between origins and destinations

SELECT
    max(cost)
FROM
    distance
WHERE
    start_id IN (SELECT id FROM point WHERE od_id IS NOT NULL) AND
    end_id IN (SELECT id FROM point WHERE od_id IS NOT NULL)
