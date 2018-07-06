--'create_ring_total.sql' creates 'ring_total' table, containing data on id of origin-destination point, ring placement of this point, numbers of destinations in this ring and sum of destinations from all of the prior rings
--'ring_total' table is written by the 'insert_ring_total.sql' script

DROP TABLE IF EXISTS ring_total;
CREATE TABLE ring_total (
    od_start_id INTEGER,
    ring INTEGER,
    destinations_in REAL,
    destinations_prior REAL
);
CREATE INDEX IF NOT EXISTS ring_total_od_start_id_idx ON ring_total (od_start_id);
CREATE INDEX IF NOT EXISTS ring_total_ring_idx ON ring_total (ring);
