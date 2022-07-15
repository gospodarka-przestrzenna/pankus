DROP TABLE IF EXISTS  motion_exchange_by_id;
CREATE TABLE motion_exchange_by_id (
    start_id INTEGER,
    end_id INTEGER,
    motion_exchange REAL
);

CREATE INDEX IF NOT EXISTS motion_exchange_by_id_start_id_idx ON motion_exchange_by_id (start_id);
CREATE INDEX IF NOT EXISTS motion_exchange_by_id_end_id_idx ON motion_exchange_by_id (end_id);

INSERT INTO motion_exchange_by_id
SELECT 
    start.id,end.id,motion_exchange.motion_exchange*:fraction
FROM
    point as start,
    point as end,
    motion_exchange
WHERE
    start.od_id=motion_exchange.od_start_id AND
    end.od_id=motion_exchange.od_end_id
 ;

INSERT INTO  stress
SET stress=(stress+stressed.stress)
FROM 
    (SELECT 
        path.segment_start_id as start_id,path.segment_end_id as end_id ,sum(me.motion_exchange) as stress
    FROM
        path,
        motion_exchange_by_id as me
    WHERE
        path.start_id=me.start_id AND
        path.end_id=me.end_id
    GROUP BY
        path.segment_start_id,path.segment_end_id) as stressed
WHERE
    stressed.start_id=start_id AND
    stressed.end_id=end_id
;
DROP TABLE IF EXISTS  motion_exchange_by_id;
