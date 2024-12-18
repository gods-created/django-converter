#!/bin/sh

python manage.py makemigrations dashboard & python manage.py migrate dashboard --database=users & python manage.py runserver 0.0.0.0:8001