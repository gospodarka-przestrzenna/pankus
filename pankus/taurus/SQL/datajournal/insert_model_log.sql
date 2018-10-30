INSERT INTO model_log
SELECT
  :action_uid,
  :action,
  datetime('now'),
  :p_action_uid,
  :version
