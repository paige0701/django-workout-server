#!/bin/bash

# Migrate Database
python3 manage.py migrate --noinput

# Collect Staticfiles
python3 manage.py collectstatic --noinput

# Run Gunicorn (WSGI Server)
gunicorn --bind 0.0.0.0:8000 config.wsgi:application