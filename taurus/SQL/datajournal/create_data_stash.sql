CREATE TABLE IF NOT EXISTS data_stash (
    action_uid INTEGER,
    table_name TEXT,
    csv TEXT
);
CREATE INDEX IF NOT EXISTS data_stash_action_uid_idx ON data_stash (action_uid);
CREATE INDEX IF NOT EXISTS data_stash_table_name_idx ON data_stash (table_name);
