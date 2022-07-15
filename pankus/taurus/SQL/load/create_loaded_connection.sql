DELETE FROM connection;
INSERT INTO connection
    SELECT
        start_id,
        end_id,
        weight*(1+((load/throughput)*(load/throughput)*(load/throughput)*(load/throughput)*(load/throughput)))
    FROM
        weight_load_change
