DROP TABLE IF EXISTS od;
CREATE TABLE od (
    od_id INTEGER PRIMARY KEY,
    point TEXT,
    origins REAL,
    destinations REAL,
    selectivity REAL,
    convolution_start REAL,
    convolution_size REAL,
    convolution_intensity REAL
);
CREATE INDEX IF NOT EXISTS od_od_id_idx ON od (od_id);
CREATE INDEX IF NOT EXISTS od_point_idx ON od (point);
