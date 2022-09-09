UPDATE
	network_properties
SET
	value=(
	SELECT
		ifnull(s.load,0)
	FROM
		load as s,
		point as p1,
		point as p2
	WHERE
		network_properties.end = p2.point AND
		network_properties.start = p1.point AND
		s.start_id  = p1.id AND
		s.end_id  = p2.id
	LIMIT 1)
WHERE
	name=:name