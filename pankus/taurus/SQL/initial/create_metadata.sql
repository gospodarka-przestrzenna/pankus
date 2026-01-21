-- creating the table for static metadata of the computation 
-- it can be ex the CRS or other settings

CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);
