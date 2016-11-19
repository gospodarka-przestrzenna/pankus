DROP TABLE IF EXISTS bmst;
CREATE TABLE bmst (
    bmst_id INTEGER,
    level INTEGER,
    bmst_supernode INTEGER
);
CREATE INDEX IF NOT EXISTS bmst_bmst_id_idx ON bmst (bmst_id);
CREATE INDEX IF NOT EXISTS bmst_bmst_supernode_idx ON bmst (bmst_supernode);
CREATE INDEX IF NOT EXISTS bmst_level_idx ON bmst (level);


DROP TABLE IF EXISTS bmst_connection;
CREATE TABLE bmst_connection(
    bmst_start_id INTEGER,
    bmst_end_id INTEGER,
    weight REAL
);
CREATE INDEX IF NOT EXISTS bmst_connection_bmst_start_id_idx ON bmst_connection (bmst_start_id);
CREATE INDEX IF NOT EXISTS bmst_connection_bmst_end_id_idx ON bmst_connection (bmst_end_id);
CREATE INDEX IF NOT EXISTS bmst_connection_weight_idx ON bmst_connection (weight);


DROP TABLE IF EXISTS bmst_used_connection;
CREATE TABLE bmst_used_connection(
    bmst_start_id INTEGER,
    bmst_end_id INTEGER,
    level INTEGER,
    weight REAL
);
CREATE INDEX IF NOT EXISTS bmst_used_connection_bmst_start_id_idx ON bmst_used_connection (bmst_start_id);
CREATE INDEX IF NOT EXISTS bmst_used_connection_bmst_end_id_idx ON bmst_used_connection (bmst_end_id);
CREATE INDEX IF NOT EXISTS bmst_used_connection_level_idx ON bmst_used_connection (level);