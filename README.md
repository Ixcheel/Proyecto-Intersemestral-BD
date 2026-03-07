# Proyecto-Intersemestral-BD
Construir una API REST para un sistema de renta y devolución de películas usando  PostgreSQL con la base Pagila (DVD Rental). El foco principal: transacciones concurrentes, aislamiento, deadlocks, manejo  del SQL y triggers.

Como lo realizamos en un contenedor de Docker para evitar conflictos con los puertos nuestra liga de acceso es la siguiente:
### http://localhost:5003

Dentro del archivo config.py cambie sus credenciales de acceso a PostgreSQL
        "postgresql+psycopg2://usuario:contraseña@localhost:5432/proyecto"

## Pasos para desplegar el proyecto
### Windows
**Levantar el contenedor de Docker**


docker-compose down -v 


docker-compose up --build 

**Activar entorno virtual**

python -m venv .venv

.\.venv\Scripts\Activate.ps1 

**Instalar estas dependencias que a veces no es compatible con el docker-compose.yml y no se instalan correctamente**


pip install flask sqlalchemy flask-sqlalchemy


pip install flask-migrate              


### MacOS
**Levantar el contenedor de Docker**

docker-compose down -v


docker-compose up --build

**Activar entorno virtual**

python3 -m venv .venv


source .venv/bin/activate

**Instalar estas dependencias que a veces no es compatible con el docker-compose.yml y no se instalan correctamente**

pip3 install flask sqlalchemy flask-sqlalchemy

pip3 install flask-migrate


## Comprobar scripts sql
### Windows
Get-Content ./sql/queries.sql | docker exec -i proyecto-db psql -U postgres -d proyecto

Get-Content ./sql/triggers.sql | docker exec -i proyecto-db psql -U postgres -d proyecto

### MacOS
docker exec -i proyecto-db psql -U postgres -d proyecto < ./sql/queries.sql

docker exec -i proyecto-db psql -U postgres -d proyecto < ./sql/triggers.sql

## Comprobar scripts pgbench deadlock
### Windows
**Provocar un deadlock**

Get-Content scripts/pgbench/scriptB_deadlock.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

**Verificar deadlock**

docker logs proyecto-db --since 2m | findstr deadlock

**Verificar versión corregida**

Get-Content scripts/pgbench/scriptB_deadlock_fixed.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

### MacOS
**Provocar un Deadlock**

cat scripts/pgbench/scriptB_deadlock.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

**Verificar deadlock**

docker logs proyecto-db --since 2m | grep deadlock

**Verificar versión corregida**

cat scripts/pgbench/scriptB_deadlock_fixed.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

## Comprobar scripts pgbench hot inventory
### Windows
**Ver rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update FROM rental WHERE inventory_id = 1 AND return_date IS NULL ORDER BY rental_id;"

**Contar rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT inventory_id, COUNT(*) AS active_rentals FROM rental WHERE inventory_id = 1 AND return_date IS NULL GROUP BY inventory_id;"

**Limpiar las rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "UPDATE rental SET return_date = clock_timestamp(), last_update = clock_timestamp() WHERE inventory_id = 1 AND return_date IS NULL;"

**Correr script corregido**

Get-Content -Raw scripts/pgbench/scriptA_hot_inventory_fixed.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

**Verificar rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT inventory_id, COUNT(*) AS active_rentals FROM rental WHERE inventory_id = 1 AND return_date IS NULL GROUP BY inventory_id;"


### MacOS
**Ver rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update FROM rental WHERE inventory_id = 1 AND return_date IS NULL ORDER BY rental_id;"

**Contar rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT inventory_id, COUNT(*) AS active_rentals FROM rental WHERE inventory_id = 1 AND return_date IS NULL GROUP BY inventory_id;"

**Limpiar las rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "UPDATE rental SET return_date = clock_timestamp(), last_update = clock_timestamp() WHERE inventory_id = 1 AND return_date IS NULL;"

**Correr script corregido**

cat scripts/pgbench/scriptA_hot_inventory_fixed.sql | docker exec -i proyecto-db pgbench -U postgres -n -c 20 -j 4 -T 30 -f - proyecto

**Verificar rentas activas**

docker exec -i proyecto-db psql -U postgres -d proyecto -c "SELECT inventory_id, COUNT(*) AS active_rentals FROM rental WHERE inventory_id = 1 AND return_date IS NULL GROUP BY inventory_id;"

