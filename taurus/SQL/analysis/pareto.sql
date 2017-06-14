SELECT
    *
FROM
    model_parameters
ORDER BY
    desinations
LIMIT
    (SELECT count(*) FROM model_parameters )
