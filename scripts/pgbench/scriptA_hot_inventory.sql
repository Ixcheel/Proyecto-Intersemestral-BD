
\set iid 1
\set cid random(1, 599)
\set sid random(1, 2)

BEGIN;

SELECT COUNT(*)
FROM rental
WHERE inventory_id = :iid
  AND return_date IS NULL;

SELECT pg_sleep(0.2);

INSERT INTO rental (
    rental_date,
    inventory_id,
    customer_id,
    return_date,
    staff_id,
    last_update
)
VALUES (
    clock_timestamp(),
    :iid,
    :cid,
    NULL,
    :sid,
    clock_timestamp()
);

COMMIT;