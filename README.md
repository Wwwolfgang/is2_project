## Crear venv y activarlo, dentro del venv ejecutar
```pip install -r requirements.txt```



# CONFIG DOCKER 
## Iniciar container de base de datos postgres (si usan Docker)
```sudo docker-compose up -d```

## Para acceder al bash (si usan Docker)
```sudo docker exec -it pg_container bash```

## Para acceder a la base de datos (si usan Docker)
```psql --host=pg_container --dbname=test_db --username=root```

## To get the latest version of docker-compose in case of a problem with compose (si usan Docker)
```sudo apt remove docker-compose```
```curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/bin/docker-compose```
```sudo chmod +x /usr/bin/docker-compose```



### run
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

### Configuración de la base de datos de desarrollo
'NAME': 'test_db',
'USER': 'root',
'PASSWORD': 'root',

## Git
```git remote set-url origin https://<USERNAME>:<PASSWORD>@bitbucket.org/path/to/repo.git ```

## Dentro del .env tambien encuentran el id y el secret para el sso 
## Guía para ver la configuración del sso https://www.section.io/engineering-education/django-google-oauth/
```sudo docker exec pg_container pg_dump -Fc -U root test_db > db.dump```