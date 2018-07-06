--'update_origins.sql' updates 'model_parameters' table with data exported from python script

UPDATE model_parameters
SET origins=:origins
WHERE od_id=:od_id
