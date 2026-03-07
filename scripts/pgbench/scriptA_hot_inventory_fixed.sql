-- Script A 
-- Simula múltiples clientes intentando rentar el mismo inventory_id
-- con control correcto de concurrencia.


\set iid 1
\set cid random(1, 599)
\set sid random(1, 2)

BEGIN;

SELECT inventory_id
FROM inventory
WHERE inventory_id = :iid
FOR UPDATE;

INSERT INTO rental (
    rental_date,
    inventory_id,
    customer_id,
    return_date,
    staff_id,
    last_update
)
SELECT
    clock_timestamp(),
    :iid,
    :cid,
    NULL,
    :sid,
    clock_timestamp()
WHERE NOT EXISTS (
    SELECT 1
    FROM rental
    WHERE inventory_id = :iid
      AND return_date IS NULL
);

COMMIT;