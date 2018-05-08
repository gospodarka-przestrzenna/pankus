--'insert_motion_exchange.sql' writes 'motion_excahnge' table with data from 'motion_exchange' function from 'intervening_opportunity' script

INSERT INTO motion_exchange VALUES (
    :sd_start_id,
    :sd_end_id,
    :motion_exchange
)
