# Proyecto-Intersemestral-BD
Construir una API REST para un sistema de renta y devolución de películas usando  PostgreSQL con la base Pagila (DVD Rental). El foco principal: transacciones concurrentes, aislamiento, deadlocks, manejo  del SQL y triggers.

## Pasos para desplegar el proyecto
### Windows
docker-compose down -v
docker-compose up --build

python -m venv .venv

.\.venv\Scripts\Activate.ps1

### MacOS
docker-compose down -v
docker-compose up --build

python3 -m venv .venv

source .venv/bin/activate
