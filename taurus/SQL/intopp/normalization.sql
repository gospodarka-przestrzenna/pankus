DROP TABLE IF EXISTS temp_motion_exchange_fraction_total;
CREATE TABLE temp_motion_exchange_fraction_total (
    sd_start_id INTEGER,
    total FLOAT
);

INSERT INTO  temp_motion_exchange_fraction_total
SELECT
    sd_start_id,
    sum(fraction)
FROM
    motion_exchange_fraction
GROUP BY
    sd_start_id;


UPDATE motion_exchange_fraction
SET fraction=(
    SELECT
        motion_exchange_fraction.fraction/tmeft.total
    FROM
        temp_motion_exchange_fraction_total as tmeft
    WHERE
        tmeft.sd_start_id=motion_exchange_fraction.sd_start_id
    LIMIT 1
    );

UPDATE motion_exchange
SET motion_exchange=(
    SELECT
        motion_exchange.motion_exchange/tmeft.total
    FROM
        temp_motion_exchange_fraction_total as tmeft
    WHERE
        tmeft.sd_start_id=motion_exchange.sd_start_id
    LIMIT 1
    );
