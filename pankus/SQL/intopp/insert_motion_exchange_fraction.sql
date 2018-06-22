--'insert_motion_exchange_fraction.sql' writes 'motion_excahnge_fraction' table with data from 'motion_exchange' function from 'intervening_opportunity' script

INSERT INTO motion_exchange_fraction VALUES (
    :sd_start_id,
    :sd_end_id,
    :fraction
)
