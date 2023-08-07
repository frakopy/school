## Requirements

[Install Docker](https://docs.docker.com/engine/install/)

[Install Docker Compose (Linux)](https://docs.docker.com/compose/install/#install-compose-on-linux-systems) (Not necessary if using **Docker Desktop for Mac** o **Docker Desktop for Windows**)

[Install Jinja2 Command-Line Tool](https://pypi.org/project/j2cli/)

# Local development
## Start app (FAST WAY)

You can start the project via the _run.sh_ script

```
./run.sh
```

## Start app (MANUALLY)
### Start DB

```
docker-compose up -d db
```

The ./volumes/mysql folder will be created, this is for persisting data, if you want to load a new dump or empty your db, this folder can be eliminated.

### Start app

```
docker-compose up -d cit
```

### Stop app

```
docker-compose down
```

## Fresh install
You may want to create a django-admin superuser:

```
docker-compose exec web python manage.py createsuperuser
```

And collect grapelli grapelly admin media files:

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

# Questions?

Just ask!
