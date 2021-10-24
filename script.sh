#!/bin/bash
su -c "psql -c 'DROP DATABASE test_db;'" -l postgres
su -c "createdb test_db" -l postgres
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata datos.json
python manage.py shell -c "exec(open('datos.py').read())"
gunicorn is_project.wsgi 192.168.0.0:8000