--'create_ring.sql' creates table 'ring' containing data on id of a pair of source-destiantion points and number of ring which the second point is placed in (in relation to the first point).
--Table 'ring' is written by the 'insert_ring_uniform.sql' and 'insert_ring_weighted.sql' scripts

DROP TABLE IF EXISTS ring;
CREATE TABLE ring (
    sd_start_id INTEGER,
    sd_end_id INTEGER,
    ring INTEGER
);
CREATE INDEX IF NOT EXISTS ring_sd_start_id_idx ON ring (sd_start_id);
CREATE INDEX IF NOT EXISTS ring_sd_end_id_idx ON ring (sd_end_id);
CREATE INDEX IF NOT EXISTS ring_ring_idx ON ring (ring);
