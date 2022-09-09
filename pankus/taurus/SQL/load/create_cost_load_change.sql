
DROP TABLE IF EXISTS weight_load_change;
CREATE TABLE weight_load_change(
    start_id INTEGER,
    end_id INTEGER,
    load REAL,
	throughput REAL,
	weight REAL
);
CREATE INDEX IF NOT EXISTS weight_load_change_start_id_idx ON weight_load_change (start_id);
CREATE INDEX IF NOT EXISTS weight_load_change_end_id_idx ON weight_load_change (end_id);
