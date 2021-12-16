#!/bin/bash
docker stop portal_postgres
docker rm portal_postgres
docker run --name portal_postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres
sleep 2s
python manage.py migrate reporting


# docker run -d --network=host \
#   -e "DB_DBNAME=postgres" \
#   -e "DB_PORT=5432" \
#   -e "DB_USER=postgres" \
#   -e "DB_HOST=127.0.0.1" \
#   -e "POSTGRES_HOST_AUTH_METHOD=trust" \
#   --name portal_postgres postgres
