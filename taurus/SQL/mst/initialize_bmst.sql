INSERT INTO bmst
SELECT DISTINCT
    bmst_start_id,
    0,
    bmst_start_id
FROM
    bmst_connection;