CREATE TABLE temp_compute_values  (
          id integer,
          destinations real
          );

WITH fcs(id,_floor,celling) AS (
    SELECT
        od_id,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :floor_name LIMIT 1)+0 as _floor,
        (select value from od_properties
        where od_geometry.od_id=od_id and name = :celling_name LIMIT 1)+0 as celling
    FROM
        od_geometry
),
sums(surplus, deficyt, max_surplus, max_deficyt) AS(
    SELECT
        SUM(
            CASE 
                WHEN model_parameters.destinations > fcs.celling then model_parameters.destinations-fcs.celling
                ELSE 0
            END
        ) as surplus,
        SUM(
            CASE
                WHEN model_parameters.destinations < fcs._floor then fcs._floor-model_parameters.destinations
                ELSE 0
            END
        ) as deficyt,
        SUM(
            CASE 
                WHEN model_parameters.destinations > fcs._floor AND
                        model_parameters.destinations < fcs.celling 
                        THEN fcs.celling-model_parameters.destinations
                ELSE 0
            END
        ) as maximal_surplus,
        SUM(
            CASE 
                WHEN model_parameters.destinations > fcs._floor AND
                        model_parameters.destinations < fcs.celling 
                        THEN model_parameters.destinations-fcs._floor
                ELSE 0
            END
        ) as maximal_deficyt
    FROM
        model_parameters,
        fcs
    WHERE 
        model_parameters.od_id == fcs.id
),
chg_fractions(bump_fraction,reduce_fraction) AS (
    SELECT
        CASE
            WHEN sums.surplus > sums.deficyt AND (sums.surplus - sums.deficyt) > sums.max_surplus THEN
                1/0
            ELSE
                CASE
                    WHEN sums.surplus > sums.deficyt THEN
                        (sums.surplus - sums.deficyt) / sums.max_surplus
                    ELSE
                        0
                END
        END as bump_fraction,
        CASE
            WHEN sums.deficyt > sums.surplus AND (sums.deficyt - sums.surplus) > sums.max_deficyt THEN
                1/0 
            ELSE 
                CASE
                    WHEN sums.deficyt > sums.surplus THEN
                        (sums.deficyt - sums.surplus) / sums.max_deficyt
                    ELSE
                        0
                END
        END as reduce_fraction
    FROM
        sums
),
compute_values(od_id,destinations) AS (
    SELECT
        mp.od_id,
        CASE
            WHEN mp.destinations < fcs._floor THEN fcs._floor
            WHEN mp.destinations > fcs.celling THEN fcs.celling
            ELSE
                CASE
                    WHEN chg_fractions.reduce_fraction > 0 THEN
                        mp.destinations - (mp.destinations - fcs._floor) * ( chg_fractions.reduce_fraction)
                    WHEN chg_fractions.bump_fraction > 0 THEN
                        mp.destinations + (fcs.celling - mp.destinations) * ( chg_fractions.bump_fraction)
                    ELSE
                        mp.destinations
                END
        END
    FROM
        model_parameters as mp,
        fcs,
        chg_fractions
    WHERE
        fcs.id == mp.od_id
)
INSERT INTO temp_compute_values
SELECT od_id, destinations 
FROM compute_values;

UPDATE model_parameters
SET destinations = (SELECT destinations FROM temp_compute_values WHERE temp_compute_values.id = model_parameters.od_id)
WHERE EXISTS (SELECT * FROM temp_compute_values WHERE temp_compute_values.id = model_parameters.od_id);

DROP TABLE temp_compute_values;