DROP TABLE IF EXISTS distance_ring;
CREATE TABLE distance_ring (
    start_id INTEGER,
    end_id INTEGER,
    predecessor_id INTEGER,
    successor_id INTEGER,
    weight REAL
);
--CREATE INDEX IF NOT EXISTS distance_ring_start_id_idx ON distance_ring (start_id);
--CREATE INDEX IF NOT EXISTS distance_ring_end_id_idx ON distance_ring (end_id);
CREATE INDEX IF NOT EXISTS distance_ring_weight_id_idx ON distance_ring (weight);

DROP TABLE IF EXISTS used_points;
CREATE TABLE used_points (
    id INTEGER
);
----CREATE INDEX IF NOT EXISTS distance_ring_start_id_idx ON distance_ring (start_id);
----CREATE INDEX IF NOT EXISTS distance_ring_end_id_idx ON distance_ring (end_id);
CREATE INDEX IF NOT EXISTS used_id_idx ON used (id);

