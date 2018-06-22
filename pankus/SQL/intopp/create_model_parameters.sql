--'create_model_parameteres.sql' creates 'model_parameters' table containing data on model parameters - sd id of a point, number of sources, number of destinations, selectivity and convolution.
--'model_parameters' table is written by the 'insert_model_parameters.sql' and 'update_sd_selectivity.sql' scripts

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
