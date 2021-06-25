### Reservation task

- Build using django and drf;
- Uses Gunicorn + NGINX + PostgreSQL;

To run:
```
    $ cd corner_case
    $ docker-compose up -d
```

Create first user:
```
$ docker-compose run web python manage.py createsuperuser
```
And fill out first user info

API documentation can be found at `/swagger-ui`