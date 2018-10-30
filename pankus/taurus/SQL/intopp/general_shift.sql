UPDATE model_parameters
SET
    destinations=(
        (SELECT sum(motion_exchange) FROM motion_exchange WHERE od_end_id=model_parameters.od_id)*
        (SELECT sum(destinations) FROM model_parameters)/(SELECT sum(origins) FROM model_parameters)
    ),
    origins=(SELECT sum(motion_exchange) FROM motion_exchange WHERE od_end_id=model_parameters.od_id)
