INSERT INTO bmst_connection
SELECT
    start_id,
    end_id,
    cost
FROM
    distance;