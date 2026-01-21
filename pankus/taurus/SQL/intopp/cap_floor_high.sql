-- each floor must be less than sum of destinations

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
)
SELECT
    count(*) == 0
FROM
    model_parameters,
    fcs,
    destinations_sum
WHERE
    model_parameters.od_id == fcs.id and 
    fcs._floor > destinations_sum.sum;