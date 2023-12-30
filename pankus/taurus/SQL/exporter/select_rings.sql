--
SELECT
	g_start.point,
	g_start.od_id,
	g_end.od_id,
	(SELECT ring FROM ring WHERE od_start_id=g_start.od_id AND od_end_id=g_end.od_id) as ring,
FROM
	od_geometry as g_start,
	od_geometry as g_end
WHERE
	g_start.od_id IN (SELECT od_id FROM point WHERE od_id IS NOT NULL) AND
	g_start in :list_of_points