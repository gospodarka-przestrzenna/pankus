--'create_stress.sql' creates 'stress' table, containing data on pairs of connected points and stress of these connections

DROP TABLE IF EXISTS stress;
CREATE TABLE stress(
    start_id INTEGER,
    end_id INTEGER,
    stress REAL
);
CREATE INDEX IF NOT EXISTS stress_start_id_idx ON stress (start_id);
CREATE INDEX IF NOT EXISTS stress_end_id_idx ON stress (end_id);
