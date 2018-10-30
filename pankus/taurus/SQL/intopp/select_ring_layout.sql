--


select
    od_id,
    (select value from od_properties
    where od_geometry.od_id=od_id and name = :fixed_rings_name LIMIT 1)
from
    od_geometry
