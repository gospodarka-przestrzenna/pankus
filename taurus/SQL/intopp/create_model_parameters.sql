DROP TABLE IF EXISTS model_parameters;
CREATE TABLE model_parameters(
    sd_id INTEGER,
    sources REAL,
    destinations REAL,
    selectivity REAL,
    convolution_start REAL,
    convolution_size REAL,
    convolution_intensity REAL
);
CREATE INDEX IF NOT EXISTS model_parameters_sd_id_idx ON model_parameters (sd_id);