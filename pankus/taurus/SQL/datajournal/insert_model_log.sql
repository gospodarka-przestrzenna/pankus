INSERT INTO model_log
SELECT
  :action_uid,
  :action,
  :datetime,
  :p_action_uid,
  :version
