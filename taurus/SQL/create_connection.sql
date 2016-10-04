DROP TABLE IF EXISTS connection;
CREATE TABLE connection(
    start_id INTEGER,
    end_id INTEGER,
    weight REAL
);
CREATE INDEX IF NOT EXISTS connection_start_id_idx ON point (start_id);
CREATE INDEX IF NOT EXISTS connection_end_id_idx ON point (end_id);