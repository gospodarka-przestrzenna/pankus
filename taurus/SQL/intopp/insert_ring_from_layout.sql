INSERT INTO ring
SELECT DISTINCT
      p1.od_id as p1id,
      p2.od_id as p2id,
      rl.ring_number as ring_number
  FROM
      point as p1,
      point as p2,
      distance as d,
      ring_layout as rl
  WHERE
      p1.od_id NOT NULL AND
      p2.od_id NOT NULL AND
      d.start_id=p1.id AND
      d.end_id=p2.id AND
      rl.od_id=p1.od_id AND
      rl.prior_rings_size <= d.weight AND
      rl.prior_rings_size + rl.ring_size > d.weight
