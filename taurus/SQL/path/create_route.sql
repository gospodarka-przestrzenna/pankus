DROP TABLE IF EXISTS path;
CREATE TABLE network (
    sd_start_id INTEGER,
    sd_end_id INTEGER,
    start_id INTEGER,
    end_id INTEGER,

);
CREATE INDEX IF NOT EXISTS network_start_idx ON network (start);
CREATE INDEX IF NOT EXISTS network_end_idx ON network (end);

