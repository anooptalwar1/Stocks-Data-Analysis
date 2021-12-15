## Local Development (FOR PC)

1. Select the approporiate virtual environment or create a new one

2. Run `pip install -r requirements.txt`
    This will install django.

    Note: arrowpy will throw an error on Python 3.8 (they have not created a binary to support install via pip install). 

    If this error happens to you, try using Python 3.7

3. Start PostgreSQL instance

   `docker run --name portal_postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres`

4. Configure Django to use local PostgreSQL instance
    - Edit DATABASES section in settings.py

        ```
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432'
        ```

5. Run `python manage.py migrate reporting`

6. Load Dummy Data
    - Download database dump - [dump_08062020.sql] (Request access, if needed)

    - Copy into your container.
        ```
        docker cp /path/to/dump <container_id>:/
        ```

    - Restore using pg_restore
        ```
        docker exec -ti <container_id> pg_restore --dbname=postgres --schema=public --data-only --format=c --username=postgres --host=localhost --port=5432 --disable-triggers dump_oct9_2020.sql
        ```

7. Application requires authenticated access. 
     - Create your user in users table
     - Create Environment Variables: 
         - env: dev
         - user: {email used in previous step}

8. Run `python manage.py runserver`

## Local Development (FOR Mac)

### Setup python virtual environment and install requirements
```
python3.7 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Create new container, set container variable
```
docker run --name portal_postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres
CONTAINER=$(docker inspect --format="{{.Id}}" portal_postgres)
python3.7 manage.py migrate reporting 0001_initial
```
### Load Dummy data
Download database dump - [dump_08042020.sql](https://drive.google.com/file/d/1iOXLnCSzv-VpO11kBMzlvm7I_YuDmM1p/view?usp=sharing) (Request access, if needed)

```
docker cp /path/to/dump $CONTAINER:/
docker exec -ti $CONTAINER pg_restore --dbname=postgres --schema=public --data-only --format=c --username=postgres --host=localhost --port=5432 dump_08042020.sql
```

### Finish DB migration
```
python3.7 manage.py migrate reporting
python3.7 manage.py runserver
```


## Production Run

`gunicorn sda.wsgi`

### How to build the Docker Image
```
docker build -t portal-admin:v0.1 .
docker run --rm -d -p 8081:8000 portal-admin:v0.1

Open in browser http://localhost:8081 OR curl http://localhost:8081

```
### deployment on kubernetes cluster
In ../dram/portal_deployment.yaml file, replace line number 22 i.e. image: PORTAL_IMAGE with the pushed portal docker image (that we have created earlier).
Then:
```
kubectl apply -f portal_deployment.yaml -n <NAMESPACE>

Open in browser http://<NODE-IP>:32324 OR curl http://<NODE-IP>:32324

```

## Generating migrations
```
python manage.py migrate reporting
```
