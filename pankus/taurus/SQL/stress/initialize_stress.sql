--just zeroed stress table

INSERT INTO stress
SELECT
	start_id,end_id,0
FROM
	connection

