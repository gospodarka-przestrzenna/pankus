DROP TABLE IF EXISTS sd;
CREATE TABLE sd (
    sd_id INTEGER PRIMARY KEY,
    point TEXT,
    sources REAL,
    destinations REAL,
    selectivity REAL,
    convolution_start REAL,
    convolution_size REAL,
    convolution_intensity REAL
);
CREATE INDEX IF NOT EXISTS sd_sd_id_idx ON sd (sd_id);
CREATE INDEX IF NOT EXISTS sd_point_idx ON sd (point);
