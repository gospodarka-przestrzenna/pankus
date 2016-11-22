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
