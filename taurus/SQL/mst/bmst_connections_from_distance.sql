INSERT INTO bmst_connection
SELECT
    start_id,
    end_id,
    weight
FROM
    distance;