--creating 'sd_geometry' and 'sd_parameters' tables, containing data on source-destination points related to the network described in the 'network_geometry' table. Each row of 'sd_properties' table contains data on sd id of a point, name of parameter describing the point and its value. Each row of 'sd_geometry' table contains data on sd id of a point and its coordinates.
--'sd_geometry' and 'sd_properties' tables are written by the 'import_sd_geometry.sql' and 'import_sd_properties.sql' scripts

DROP TABLE IF EXISTS sd_geometry;
CREATE TABLE sd_geometry (
    sd_id INTEGER,
    point TEXT
);

CREATE INDEX IF NOT EXISTS sd_geometry_sd_id_idx ON sd_geometry (sd_id);
CREATE INDEX IF NOT EXISTS sd_geometry_point_idx ON sd_geometry (point);

DROP TABLE IF EXISTS sd_properties;
CREATE TABLE sd_properties (
    sd_id INTEGER,
    name TEXT,
    value TEXT
);

CREATE INDEX IF NOT EXISTS sd_properties_sd_id_idx ON sd_properties (sd_id);
CREATE INDEX IF NOT EXISTS sd_properties_point_idx ON sd_properties (name);
