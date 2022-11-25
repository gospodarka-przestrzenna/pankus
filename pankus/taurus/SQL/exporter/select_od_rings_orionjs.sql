--
with 
  all_od(od_start_id) as
    (select distinct od_start_id from ring),
  all_r(ring) as
    (select distinct ring from ring)
select
    all_od.od_start_id,
	all_r.ring,
	(select 
		GROUP_CONCAT(od_end_id, ' ')
	from 
		ring
	where
		ring.od_start_id=all_od.od_start_id and
		ring.ring=all_r.ring
  	order by
    	od_end_id
	)
from 
	  all_od,
	  all_r