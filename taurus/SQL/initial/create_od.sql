--creating 'od_geometry' and 'od_parameters' tables, containing data on origin-destination points related to the network described in the 'network_geometry' table. Each row of 'od_properties' table contains data on od id of a point, name of parameter describing the point and its value. Each row of 'od_geometry' table contains data on od id of a point and its coordinates.
--'od_geometry' and 'od_properties' tables are written by the 'import_od_geometry.sql' and 'import_od_properties.sql' scripts

DROP TABLE IF EXISTS od_geometry;
CREATE TABLE od_geometry (
    od_id INTEGER,
    point TEXT
);

CREATE INDEX IF NOT EXISTS od_geometry_od_id_idx ON od_geometry (od_id);
CREATE INDEX IF NOT EXISTS od_geometry_point_idx ON od_geometry (point);

DROP TABLE IF EXISTS od_properties;
CREATE TABLE od_properties (
    od_id INTEGER,
    name TEXT,
    value TEXT
);

CREATE INDEX IF NOT EXISTS od_properties_od_id_idx ON od_properties (od_id);
CREATE INDEX IF NOT EXISTS od_properties_point_idx ON od_properties (name);
