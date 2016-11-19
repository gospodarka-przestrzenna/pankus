DROP TABLE IF EXISTS ring;
CREATE TABLE ring (
    sd_start_id INTEGER,
    sd_end_id INTEGER,
    ring INTEGER
);
CREATE INDEX IF NOT EXISTS ring_sd_start_id_idx ON ring (sd_start_id);
CREATE INDEX IF NOT EXISTS ring_sd_end_id_idx ON ring (sd_end_id);
CREATE INDEX IF NOT EXISTS ring_ring_idx ON ring (ring);