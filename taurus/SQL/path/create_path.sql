DROP TABLE IF EXISTS network;
CREATE TABLE network (
    linestring TEXT,
    weight REAL,
    start TEXT,
    end TEXT,
    throughput REAL
);
CREATE INDEX IF NOT EXISTS network_start_idx ON network (start);
CREATE INDEX IF NOT EXISTS network_end_idx ON network (end);

