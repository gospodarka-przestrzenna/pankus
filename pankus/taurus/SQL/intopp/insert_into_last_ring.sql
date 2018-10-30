UPDATE ring
SET ring =
    (SELECT
        max(ifnull(r.ring,0))+1
    FROM
        ring as r)
WHERE
    ring is NULL