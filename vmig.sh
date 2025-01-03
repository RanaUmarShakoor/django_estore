#!/bin/bash

python manage.py makemigrations
python manage.py makemigrations core
python manage.py migrate
