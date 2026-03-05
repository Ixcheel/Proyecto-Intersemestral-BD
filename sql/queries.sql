-- Manejo de SQL
-- Window function

-- Q1 — Top 10 clientes por gasto con ranking

-- Q2 — Top 3 películas por tienda (por # de rentas)
WITH top3 AS(
	SELECT f.title, i.store_id, f.film_id,
	COUNT(r.rental_id) AS rentals_counts,
	ROW_NUMBER() OVER(
		PARTITION BY i.store_id
		ORDER BY COUNT(r.rental_id) DESC
	) AS rn
	FROM Film as f
	JOIN Inventory as i ON  f.film_id = i.film_id
	JOIN Rental as r ON i.inventory_id = r.inventory_id
	GROUP BY f.title, i.store_id, f.film_id
)
SELECT *
FROM top3
WHERE rn <=3;

-- CTES
-- Q3 — Inventario disponible por tienda (CTE)
WITH unavailable_rentals AS(
	SELECT inventory_id
	FROM Rental
	WHERE return_date is NULL)

SELECT i.store_id, COUNT(i.inventory_id) AS available_inventory_count
FROM Inventory AS i
LEFT JOIN unavailable_rentals AS u ON i.inventory_id = u.inventory_id
WHERE u.inventory_id is NULL
GROUP BY store_id;

-- Q4 — Análisis de retrasos: rentas tardías agregadas por categoría (CTE)

-- Consultas operativas
-- Q5 — Auditoría: pagos sospechosos
-- Enfoque en pagos repetidos el mismo día por el mismo cliente y monto
SELECT payment_id, customer_id, amount, payment_date, 'Pago repetido' AS flag_reason
FROM Payment
WHERE (customer_id, amount, DATE(payment_date)) IN (
    SELECT customer_id, amount, DATE(payment_date)
    FROM Payment
    GROUP BY customer_id, amount, DATE(payment_date)
    HAVING COUNT(*) > 1
);

-- Excluimos el umbral porque no hay cantidades inusuales despues de checar la información de la tabla simplemente cuenta con pagos repetidos

-- Q6 — “Clientes con riesgo” (mora)

-- Q7 — Integridad/consistencia: inventario con rentas activas duplicadas
SELECT inventory_id, ARRAY_AGG(rental_id ORDER BY rental_id) AS rental_ids, COUNT(*) AS active_rentals_count
FROM Rental
WHERE return_date IS NULL
GROUP BY inventory_id
HAVING COUNT(*) > 1

-- Manejo de SQL
-- Window function

-- Q1 — Top 10 clientes por gasto con ranking

-- Q2 — Top 3 películas por tienda (por # de rentas)
WITH top3 AS(
	SELECT f.title, i.store_id, f.film_id,
	COUNT(r.rental_id) AS rentals_counts,
	ROW_NUMBER() OVER(
		PARTITION BY i.store_id
		ORDER BY COUNT(r.rental_id) DESC
	) AS rn
	FROM Film as f
	JOIN Inventory as i ON  f.film_id = i.film_id
	JOIN Rental as r ON i.inventory_id = r.inventory_id
	GROUP BY f.title, i.store_id, f.film_id
)
SELECT *
FROM top3
WHERE rn <=3;

-- CTES
-- Q3 — Inventario disponible por tienda (CTE)
WITH unavailable_rentals AS(
	SELECT inventory_id
	FROM Rental
	WHERE return_date is NULL)

SELECT i.store_id, COUNT(i.inventory_id) AS available_inventory_count
FROM Inventory AS i
LEFT JOIN unavailable_rentals AS u ON i.inventory_id = u.inventory_id
WHERE u.inventory_id is NULL
GROUP BY store_id;

-- Q4 — Análisis de retrasos: rentas tardías agregadas por categoría (CTE)

-- Consultas operativas
-- Q5 — Auditoría: pagos sospechosos
-- Enfoque en pagos repetidos el mismo día por el mismo cliente y monto
SELECT payment_id, customer_id, amount, payment_date, 'Pago repetido' AS flag_reason
FROM Payment
WHERE (customer_id, amount, DATE(payment_date)) IN (
    SELECT customer_id, amount, DATE(payment_date)
    FROM Payment
    GROUP BY customer_id, amount, DATE(payment_date)
    HAVING COUNT(*) > 1
);

-- Q6 — “Clientes con riesgo” (mora)

-- Q7 — Integridad/consistencia: inventario con rentas activas duplicadas
SELECT inventory_id, ARRAY_AGG(rental_id ORDER BY rental_id) AS rental_ids, COUNT(*) AS active_rentals_count
FROM Rental
WHERE return_date IS NULL
GROUP BY inventory_id
HAVING COUNT(*) > 1
ORDER BY active_rentals_count DESC;