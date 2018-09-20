UPDATE ring
SET ring = ring+1
WHERE
	---not empty set contains current element if its distance is >0
	EXISTS
	(select
		*
	from
		distance,
		point as p1,
		point as p2
	where
		p1.od_id = ring.od_start_id  and
		p2.od_id=ring.od_end_id and
		p1.id=distance.start_id and
		p2.id=distance.end_id and
		distance.weight>0 )
	-- -- not empty set of elements in ring 0 where distance >0 (forbids unnecessary bumps)
	-- AND  exists
	-- (select
	-- 	*
	-- from
	-- 	distance,
	-- 	point as p1,
	-- 	point as p2,
	-- 	ring as r
	-- where
	-- 	p1.od_id = r.od_start_id  and
	-- 	p2.od_id=r.od_end_id and
	-- 	p1.id=distance.start_id and
	-- 	p2.id=distance.end_id and
	-- 	distance.weight>0 and
	-- 	r.ring=0
	-- )
