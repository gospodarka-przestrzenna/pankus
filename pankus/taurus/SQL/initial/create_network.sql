--create_network.sql creates tables 'network_geometry' and 'network_properties'. Each row of table 'network_geometry' contains data on start and end of a network segment and its description. Each row of 'network_properties' table contains data on start and end of a network segment, name of parameter describing this segment and value of the parameter.
--'network_geometry' table is written by 'import_network_geometry.sql' script
--'network_properties' table is written by 'import_network_properties.sql' script


DROP TABLE IF EXISTS network_geometry;
CREATE TABLE network_geometry (
    start TEXT,
    end TEXT,
    linestring TEXT
);

CREATE INDEX IF NOT EXISTS network_geometry_start_idx ON network_geometry (start);
CREATE INDEX IF NOT EXISTS network_geometry_end_idx ON network_geometry (end);


DROP TABLE IF EXISTS network_properties;
CREATE TABLE network_properties (
    start TEXT,
    end TEXT,
    name TEXT,
    value TEXT
);

CREATE INDEX IF NOT EXISTS network_properties_start_idx ON network_properties (start);
CREATE INDEX IF NOT EXISTS network_properties_end_idx ON network_properties (end);
