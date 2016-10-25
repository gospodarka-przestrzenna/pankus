UPDATE model_parameters
SET
    destinations=(
        (SELECT sum(motion_exchange) FROM motion_exchange WHERE sd_end_id=model_parameters.sd_id)*
        (SELECT sum(destinations) FROM model_parameters)/(SELECT sum(sources) FROM model_parameters)
    )

