select
	odp1,
	odp2
From
	(select
		p1.sd_id as odp1,
		p2.sd_id as odp2
	from
		point as p1,
		point as p2) as od_p1p2
	left join ring
	on
		od_p1p2.odp1=ring.sd_start_id and
		od_p1p2.odp2=ring.sd_end_id
where
	ring is null
