# clova-annotation

## Purpose

## Structure
* Frontend (`/front`): Vue.js
* Backend (`/server`) : Django + PostgreSQL

## Server Setup
* Assume that  `docker` and `docker-compose` are installed.
* Whenever `server/Dockerfile` is updated, run `docker-compose build`!

```
docker-compose up 
```
* `-d` option : running server on background

## Migration & Create admin

```
docker-compose exec server python manage.py makemigrations
docker-compose exec server python manage.py migrate
```
will reflect the updates in `models.py`.

```
docker-compose exec server python manage.py createsuperuser
```
helps creating an admin account.

## Server Off
```
docker-compose down 
```

## To-do's
[ ] Migration volume on local
[ ] Publish docker image on dockerhub
[ ] Deploy server on AWS with docker image.
