DROP TABLE IF EXISTS point;
CREATE TABLE point (
    point TEXT,
    id INTEGER,
    sd_id INTEGER
);
CREATE INDEX IF NOT EXISTS point_id_idx ON point (id);
CREATE INDEX IF NOT EXISTS point_sd_id_idx ON point (sd_id);