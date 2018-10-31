--'create_ring.sql' creates table 'ring' containing data on id of a pair of origin-destiantion points and number of ring which the second point is placed in (in relation to the first point).
--Table 'ring' is written by the 'insert_ring_uniform.sql' and 'insert_ring_weighted.sql' scripts

DROP TABLE IF EXISTS ring;
CREATE TABLE ring (
    od_start_id INTEGER,
    od_end_id INTEGER,
    ring INTEGER
);
CREATE INDEX IF NOT EXISTS ring_od_start_id_idx ON ring (od_start_id);
CREATE INDEX IF NOT EXISTS ring_od_end_id_idx ON ring (od_end_id);
CREATE INDEX IF NOT EXISTS ring_ring_idx ON ring (ring);
