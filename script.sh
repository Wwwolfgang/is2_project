#!/bin/bash
sudo su postgres $(psql "DROP DATABASE test_db;EXIT;";createdb test_db)
./manage.py makemigrations
./manage.py migrate
django-admin loaddata datos.json
./manage.py shell < datos.py
gunicorn is_project.wsgi