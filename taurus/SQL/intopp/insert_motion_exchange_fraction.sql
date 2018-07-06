--'insert_motion_exchange_fraction.sql' writes 'motion_excahnge_fraction' table with data from 'motion_exchange' function from 'intervening_opportunities' script

INSERT INTO motion_exchange_fraction VALUES (
    :od_start_id,
    :od_end_id,
    :fraction
)
