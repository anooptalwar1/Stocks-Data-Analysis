#!/bin/bash
docker stop portal_postgres
docker rm portal_postgres
docker run --name portal_postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres
sleep 2s
python manage.py migrate reporting