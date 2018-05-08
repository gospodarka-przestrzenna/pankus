--'create_connection.sql' creates 'connection' table, containing data on pairs of connected points and weights of these connections

DROP TABLE IF EXISTS connection;
CREATE TABLE connection(
    start_id INTEGER,
    end_id INTEGER,
    weight REAL
);
CREATE INDEX IF NOT EXISTS connection_start_id_idx ON connection (start_id);
CREATE INDEX IF NOT EXISTS connection_end_id_idx ON connection (end_id);
