DROP TABLE IF EXISTS ring_total;
CREATE TABLE ring_total (
    sd_start_id INTEGER,
    ring INTEGER,
    destinations_in REAL,
    destinations_prior REAL
);
CREATE INDEX IF NOT EXISTS ring_total_sd_start_id_idx ON ring_total (sd_start_id);
CREATE INDEX IF NOT EXISTS ring_total_ring_idx ON ring_total (ring);