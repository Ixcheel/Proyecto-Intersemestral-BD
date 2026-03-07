
-- Script B - Deadlock reproducible



\set order random(0,1)

BEGIN;

\if :order = 0
    UPDATE store
    SET last_update = clock_timestamp()
    WHERE store_id = 1;

    SELECT pg_sleep(0.2);

    UPDATE store
    SET last_update = clock_timestamp()
    WHERE store_id = 2;
\else
    UPDATE store
    SET last_update = clock_timestamp()
    WHERE store_id = 2;

    SELECT pg_sleep(0.2);

    UPDATE store
    SET last_update = clock_timestamp()
    WHERE store_id = 1;
\endif

COMMIT;