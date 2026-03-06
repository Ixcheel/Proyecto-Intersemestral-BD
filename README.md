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
cat "C:\Ruta de acceso\sql\queries.sql" | docker exec -i inter-db psql -U postgres -d inter 

cat "C:\Ruta de acceso\sql\triggers.sql" | docker exec -i inter-db psql -U postgres -d inter 

