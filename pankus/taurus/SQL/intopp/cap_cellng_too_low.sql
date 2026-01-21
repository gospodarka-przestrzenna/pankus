-- sum of floor must be less than sum of destinations
-- sum of celling must be greater than sum of destinations
-- each floor must be less than celling

WITH fcs(id,_floor,celling) AS (
    SELECT
        od_id,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :floor_name LIMIT 1) as _floor,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :celling_name LIMIT 1) as celling
    FROM
        od_geometry
),
destinations_sum(sum) AS (
    SELECT
        sum(destinations)
    FROM
        model_parameters
),
celling_sum(sum) AS (
    SELECT
        sum(celling)
    FROM
        fcs
)
SELECT
    celling_sum.sum > destinations_sum.sum  
FROM
    destinations_sum,
    celling_sum;
