-- each floor must be less than sum of destinations
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
)
SELECT
    count(*) == 0
FROM
    model_parameters,
    fcs,
WHERE
    model_parameters.od_id == fcs.id and (
    fcs._floor > (SELECT sum(destinations) FROM model_parameters) or
    fcs.celling 
    > (SELECT sum(destinations) FROM model_parameters) or