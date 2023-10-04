UPDATE model_parameters
SET
    origins=(
        ((SELECT sum(destinations) FROM model_parameters as mp WHERE mp.od_id=model_parameters.od_id)
        /(SELECT sum(destinations) FROM model_parameters))*
        (SELECT sum(origins) FROM model_parameters)
    )
