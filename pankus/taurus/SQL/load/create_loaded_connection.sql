DELETE FROM connection;
INSERT INTO connection
    SELECT
        start_id,
        end_id,
        cost*(1+((load/throughput)*(load/throughput)*(load/throughput)*(load/throughput)*(load/throughput)))
    FROM
        cost_load_change
