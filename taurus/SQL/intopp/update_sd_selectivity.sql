--'update_sd_selectivity' updates selectivity parameter in the 'model_parameters' table

UPDATE model_parameters
SET selectivity=:selectivity;
