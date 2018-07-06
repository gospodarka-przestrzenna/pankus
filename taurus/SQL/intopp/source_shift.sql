UPDATE model_parameters
SET
    origins=(
    SELECT
        sum(motion_exchange)
    FROM
        motion_exchange
    WHERE
        od_end_id=model_parameters.od_id)
