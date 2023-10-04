WITH fcs(id,floor,celling) AS (
    SELECT
        od_id,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :floor_name LIMIT 1),
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :celling_name LIMIT 1)
    FROM
        od_geometry
),
sum_org_plan(s_org,s_planned) as (
    SELECT 
        SUM(
            roof.origins
        ),
        SUM(
            CASE 
                WHEN model_parameters.origins > fcs.celling then fcs.celling
                WHEN model_parameters.origins < fcs.floor   then fcs.floor            
                ELSE model_parameters.origins
            END
        )
    FROM
        model_parameters,
        roof,
        fcs
    WHERE 
        fcs.id == model_parameters.od_id AND
        roof.od_id == model_parameters.od_id
),
new_origins(od_id,origins) AS (
    SELECT
        mp.od_id,
        CASE
            WHEN mp.origins < fcs.floor THEN fcs.floor + r.origins * (sum_org_plan.s_org - sum_org_plan.s_planned) / sum_org_plan.s_org
            WHEN mp.origins > fcs.celling THEN fcs.celling + r.origins * (sum_org_plan.s_org - sum_org_plan.s_planned) / sum_org_plan.s_org
            ELSE mp.origins + r.origins * (sum_org_plan.s_org - sum_org_plan.s_planned) / sum_org_plan.s_org
        END
    FROM
        model_parameters as mp,
        roof as r,
        fcs,
        sum_org_plan
    WHERE
        fcs.id == r.od_id AND
        r.od_id == mp.od_id
)
UPDATE model_parameters
SET 
    origins = (
    SELECT
        origins
    FROM 
        new_origins
    WHERE 
        model_parameters.od_id == new_origins.od_id
    )