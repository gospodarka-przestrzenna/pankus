--'create_ring_layout.sql' creates table 'ring_layout' containing data on od_id and rings where it is a center.
-- Contains consecutive ring size and sum
-- Table 'ring_laout' is filled with data from od_properties

DROP TABLE IF EXISTS ring_layout;
CREATE TABLE ring_layout (
    od_id INTEGER,         -- origin id
    ring_number INTEGER,   -- ring number
    ring_size real,        -- ring size
    prior_rings_size real  -- size before current ring
);

CREATE INDEX IF NOT EXISTS ring_layout_od_id_idx ON ring_layout (od_id);
