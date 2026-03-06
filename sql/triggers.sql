-- 7.1 Trigger de auditoria
CREATE TABLE IF NOT EXISTS audit_log(
	id SERIAL PRIMARY KEY,
	event_ts TIMESTAMP DEFAULT NOW(),
	table_name TEXT,
	op TEXT,
	pk JSONB,
	old_row JSONB,
	new_row JSONB
);

CREATE OR REPLACE FUNCTION auditoria()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE v_pk JSONB;
BEGIN
	IF TG_TABLE_NAME = 'rental' THEN
		v_pk := jsonb_build_object('rental_id', COALESCE(NEW.rental_id, OLD.rental_id));
	ELSEIF TG_TABLE_NAME = 'payment' THEN
		v_pk := jsonb_build_object('payment_id', COALESCE(NEW.payment_id, OLD.payment_id));
	END IF;

	INSERT INTO audit_log(table_name, op, pk, old_row, new_row) VALUES (TG_TABLE_NAME, TG_OP, v_pk, to_json(OLD), to_json(NEW));
	RETURN NULL;
END;
$$;

-- Trigger Rental
CREATE TRIGGER trg_rental
AFTER INSERT OR UPDATE OR DELETE ON rental
FOR EACH ROW
EXECUTE FUNCTION auditoria();

-- Trigger Payment
CREATE TRIGGER trg_payment
AFTER INSERT OR UPDATE OR DELETE ON payment
FOR EACH ROW
EXECUTE FUNCTION auditoria();

-- Comprobación Rental
DELETE FROM rental WHERE rental_id = 1;
INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, return_date) VALUES ('2026-03-03 12:30:00-06',1,101,2,'2026-03-10 12:30:00-06');
UPDATE rental SET return_date = '2026-03-05 15:30:00-06' WHERE rental_id = 2;

SELECT * FROM rental;

-- Comprobación Payment
DELETE FROM payment WHERE payment_id = 16051;
INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES (101, 2, 1005, 4.99, '2022-03-03 12:45:00-06');
UPDATE payment SET customer_id = 270 WHERE payment_id = 16052;

SELECT * FROM payment;

-- Comprobación del trigger
SELECT * FROM audit_log;


-- 7.2 Trigger de regla de negocio
-- Impedir renta si el cliente supera X rentas activas.
CREATE OR REPLACE FUNCTION avoid_rental()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE active_rental INT; 
BEGIN 
    SELECT COUNT(*) 
    INTO active_rental 
    FROM Rental 
    WHERE customer_id = NEW.customer_id AND return_date IS NULL;

    IF active_rental >= 5 THEN 
        RAISE EXCEPTION 'No se puede realizar la renta ya que el cliente tendría más de 5 rentas activas.';
    END IF; 
	RETURN NEW; 
END;
$$;

CREATE TRIGGER trg_avoid_rental
BEFORE INSERT ON Rental
FOR EACH ROW
EXECUTE FUNCTION avoid_rental();