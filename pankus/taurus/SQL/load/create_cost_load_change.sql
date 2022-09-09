
DROP TABLE IF EXISTS cost_load_change;
CREATE TABLE cost_load_change(
    start_id INTEGER,
    end_id INTEGER,
    load REAL,
	throughput REAL,
	cost REAL
);
CREATE INDEX IF NOT EXISTS cost_load_change_start_id_idx ON cost_load_change (start_id);
CREATE INDEX IF NOT EXISTS cost_load_change_end_id_idx ON cost_load_change (end_id);
