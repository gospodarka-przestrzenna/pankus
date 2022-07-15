--'create_load.sql' creates 'load' table, containing data on pairs of connected points and load of these connections

DROP TABLE IF EXISTS load;
CREATE TABLE load(
    start_id INTEGER,
    end_id INTEGER,
    load REAL
);
CREATE INDEX IF NOT EXISTS load_start_id_idx ON load (start_id);
CREATE INDEX IF NOT EXISTS load_end_id_idx ON load (end_id);
