
UPDATE ring
SET ring = :ring
WHERE
    ring = :ring + 1
