-- Create table that holds roof data
-- it holds capped data after each step

DROP TABLE IF EXISTS roof;
CREATE TABLE roof (
    od_id INTEGER,
    origins FLOAT,
    destinations FLOAT
);
INSERT INTO roof
SELECT 
    od_id,
    origins,
    destinations 
FROM 
    model_parameters
