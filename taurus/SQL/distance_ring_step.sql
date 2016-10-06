INSERT INTO distance_ring
SELECT
    d.start_id,
    c.end_id,
    c.start_id,
    d.successor_id,
    d.weight+c.weight
FROM
    (select
        dd.start_id,
        dd.end_id,
        dd.predecessor_id,
        dd.successor_id,
        min(dd.weight) as weight
    from
        distance_ring as dd) as d,
    connection as c
WHERE
    c.start_id=d.end_id;

insert into distance
select
    dd.start_id,
    dd.end_id,
    dd.predecessor_id,
    dd.successor_id,
    min(dd.weight) as weight
from
    distance_ring as dd;

with
    minim(start_id,end_id,predecessor_id,successor_id,weight) AS
        (select
            dd.start_id,
            dd.end_id,
            dd.predecessor_id,
            dd.successor_id,
            min(dd.weight) as weight
        from
            distance_ring as dd)

delete from distance_ring
where  (SELECT * FROM distance_ring as d where start_id=d.start_id and end_id=d.end_id);