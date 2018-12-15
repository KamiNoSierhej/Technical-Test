# Welcome in 'Technical-Test' recruiting exercise

## setting up

### pre-requirements
Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/)

### just run these commands

1. docker-compose up --build
2. docker-compose run web python manage.py migrate

## usage

### to run server use:

docker-compose up

if you want to use ipdb:
docker-compose run --service-ports web

### to run tests use:

docker-compose run web python manage.py test

### to make and run migrations use

docker-compose run web python manage.py makemigrations

and

docker-compose run web python manage.py migrate

`Be blessed!`
