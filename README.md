## Requirements

[Install Docker](https://docs.docker.com/engine/install/)

[Install Docker Compose (Linux)](https://docs.docker.com/compose/install/#install-compose-on-linux-systems) (Not necessary if using **Docker Desktop for Mac** o **Docker Desktop for Windows**)

[Install Jinja2 Command-Line Tool](https://pypi.org/project/j2cli/)

Create the enviroment variables  in docker-compose.yml about db, hostname, user and password.


## Start app

```
docker-compose up -d
```

The ./volumes/mysql folder will be created, this is for persisting data, if you want to load a new dump or empty your db, this folder can be eliminated.


### Stop app

```
docker-compose down
```

## To create a Django superuser and create static file root, please run the following command in the project: directory:
You may want to create a django-admin superuser:

```
docker-compose exec web python manage.py createsuperuser
```

```
docker-compose exec web python manage.py collectstatic
```

## Migrations
For generating migrations

```
docker-compose exec web python manage.py makemigrations
```

For migrating

```
docker-compose exec web python manage.py migrate
```

