UPDATE
	network_properties
SET
	value=vals.value
FROM
	(SELECT
		start.point as start,end.point as end,s.stress as value
	FROM
		stress as s,
		point as start,
		point as end
	WHERE
		s.start_id=start.id AND
		s.end_id=end.id 
		) as vals
WHERE
	network_properties.start=vals.start AND
	network_properties.end=vals.end AND
	network_properties.name=:name