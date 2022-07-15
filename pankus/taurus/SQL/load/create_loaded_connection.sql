DELETE FROM connection;
INSERT INTO connection
    SELECT
        start_id,
        end_id,
        weight*(1+((stress/throughput)*(stress/throughput)*(stress/throughput)*(stress/throughput)*(stress/throughput)))
    FROM
        weight_stress_change
