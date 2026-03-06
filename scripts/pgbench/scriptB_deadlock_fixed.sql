-- Script B - Deadlock corregido

BEGIN;

UPDATE store
SET last_update = clock_timestamp()
WHERE store_id = 1;

SELECT pg_sleep(0.2);

UPDATE store
SET last_update = clock_timestamp()
WHERE store_id = 2;

COMMIT;