DROP TABLE IF EXISTS distance;
CREATE TABLE distance (
    start_id INTEGER,
    end_id INTEGER,
    predecessor_id INTEGER,
    successor_id INTEGER,
    weight REAL
);
CREATE INDEX IF NOT EXISTS distance_start_id_idx ON distance (start_id);
CREATE INDEX IF NOT EXISTS distance_end_id_idx ON distance (end_id);
CREATE INDEX IF NOT EXISTS distance_start_id_end_id_idx ON distance (start_id,end_id);
