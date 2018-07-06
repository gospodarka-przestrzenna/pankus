UPDATE model_parameters
SET
    sources=(
    SELECT
        sum(motion_exchange)
    FROM
        motion_exchange
    WHERE
        sd_end_id=model_parameters.sd_id)


