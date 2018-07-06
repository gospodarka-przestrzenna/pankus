
--'select_destinations_total.sql' exports sum of destinations from 'model_parameters' table

SELECT sum(destinations) FROM model_parameters
