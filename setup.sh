#!/bin/bash

# Run migrations
python manage.py makemigrations
python manage.py migrate
