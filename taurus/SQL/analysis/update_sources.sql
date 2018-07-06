--'update_sources.sql' updates 'model_parameters' table with data exported from python script

UPDATE model_parameters
SET sources=:sources
WHERE sd_id=:sd_id
