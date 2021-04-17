
DROP TABLE IF EXISTS weight_stress_change;
CREATE TABLE weight_stress_change(
    start_id INTEGER,
    end_id INTEGER,
    stress REAL,
	throughput REAL,
	weight REAL
);
CREATE INDEX IF NOT EXISTS weight_stress_change_start_id_idx ON weight_stress_change (start_id);
CREATE INDEX IF NOT EXISTS weight_stress_change_end_id_idx ON weight_stress_change (end_id);
