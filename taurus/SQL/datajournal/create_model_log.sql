CREATE TABLE IF NOT EXISTS model_log (
    action_uid INTEGER,
    action TEXT,
    date_time TEXT,
    parent_action_uid TEXT,
    pankus_version TEXT
);
CREATE INDEX IF NOT EXISTS model_log_action_uid_idx ON model_log (action_uid);
