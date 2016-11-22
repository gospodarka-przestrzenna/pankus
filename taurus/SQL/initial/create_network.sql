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


