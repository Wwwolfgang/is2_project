## Production README

## Setup with Docker
```sudo docker-compose -f docker-compose.yml up -d --build```

## Migrate
```sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput```

## Collect Static
```sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear```

## View logs
```sudo docker-compose -f docker-compose.yml logs -f```

## Stop 
```sudo docker-compose -f docker-compose.yml down -v```