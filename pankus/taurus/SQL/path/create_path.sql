DROP TABLE IF EXISTS path;
CREATE TABLE path (
    start_id INTEGER,
    end_id INTEGER,
    segment_id INTEGER,
    segment_start_id INTEGER,
    segment_end_id INTEGER
);	
CREATE INDEX IF NOT EXISTS path_start_id_idx ON path (start_id);
CREATE INDEX IF NOT EXISTS path_end_id_idx ON path (end_id);
CREATE INDEX IF NOT EXISTS path_segment_id_idx ON path (segment_id);
