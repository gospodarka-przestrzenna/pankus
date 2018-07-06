--create_point.sql creates 'point' table, containing data on point coordinates, its id and eventually its od id if the point is a origin-destination point
--'point' table is written by the 'insert_point.sql' script

DROP TABLE IF EXISTS point;
CREATE TABLE point (
    point TEXT,
    id INTEGER PRIMARY KEY,
    od_id INTEGER
);
CREATE INDEX IF NOT EXISTS point_id_idx ON point (id);
CREATE INDEX IF NOT EXISTS point_od_id_idx ON point (od_id);
