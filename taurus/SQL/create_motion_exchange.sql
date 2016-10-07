DROP TABLE IF EXISTS motion_exchange_fraction;
CREATE TABLE motion_exchange_fraction (
    sd_start_id INTEGER,
    sd_end_id INTEGER,
    fraction REAL
);
CREATE INDEX IF NOT EXISTS motion_exchange_fraction_sd_start_id_idx ON motion_exchange_fraction (sd_start_id);
CREATE INDEX IF NOT EXISTS motion_exchange_fraction_sd_end_id_idx ON motion_exchange_fraction (sd_end_id);

DROP TABLE IF EXISTS motion_exchange;
CREATE TABLE motion_exchange (
    sd_start_id INTEGER,
    sd_end_id INTEGER,
    motion_exchange REAL
);
CREATE INDEX IF NOT EXISTS motion_exchange_sd_start_id_idx ON motion_exchange (sd_start_id);
CREATE INDEX IF NOT EXISTS motion_exchange_sd_end_id_idx ON motion_exchange (sd_end_id);