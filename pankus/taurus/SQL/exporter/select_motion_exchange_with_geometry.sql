--

SELECT
  p1.point,
  p2.point,
  ifnull((SELECT 
    mx.motion_exchange 
  FROM
    motion_exchange as mx
  WHERE
    mx.od_start_id=p1.od_id AND
    mx.od_end_id=p2.od_id
  ),0) as motion_exchange,
  ifnull((SELECT 
    ifnull(mxf.fraction,0) 
  FROM
    motion_exchange_fraction as mxf
  WHERE
    mxf.od_start_id=p1.od_id AND
    mxf.od_end_id=p2.od_id
  ),0) as motion_exchange_fraction
FROM
  point as p1,
  point as p2
WHERE
  p1.od_id is not NULL AND
  p2.od_id is not NULL
