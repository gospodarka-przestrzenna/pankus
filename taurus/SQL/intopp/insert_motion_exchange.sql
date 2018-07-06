--'insert_motion_exchange.sql' writes 'motion_excahnge' table with data from 'motion_exchange' function from 'intervening_opportunities' script

INSERT INTO motion_exchange VALUES (
    :od_start_id,
    :od_end_id,
    :motion_exchange
)
