--'create_motion_exchange.sql' creates 'motion_exchange' and 'motion_exchange_fraction' tables, containing data on id of a motion exchange start and ed point and respectively amount of fraction of 'objects' transported from start point to the end point.
--'motion_exchange' and 'motion_excahnge_fraction' tables are written respectively by the 'insert_motion_exchange.sql' and 'insert_motion_excahnge_fraction.sql' scripts

DROP TABLE IF EXISTS motion_exchange_fraction;
CREATE TABLE motion_exchange_fraction (
    od_start_id INTEGER,
    od_end_id INTEGER,
    fraction REAL
);
CREATE INDEX IF NOT EXISTS motion_exchange_fraction_od_start_id_idx ON motion_exchange_fraction (od_start_id);
CREATE INDEX IF NOT EXISTS motion_exchange_fraction_od_end_id_idx ON motion_exchange_fraction (od_end_id);

DROP TABLE IF EXISTS motion_exchange;
CREATE TABLE motion_exchange (
    od_start_id INTEGER,
    od_end_id INTEGER,
    motion_exchange REAL
);
CREATE INDEX IF NOT EXISTS motion_exchange_od_start_id_idx ON motion_exchange (od_start_id);
CREATE INDEX IF NOT EXISTS motion_exchange_od_end_id_idx ON motion_exchange (od_end_id);
