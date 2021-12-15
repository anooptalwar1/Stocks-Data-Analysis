#!/bin/bash
set -ev
python3 manage.py migrate reporting
python manage.py sqlsequencereset reporting
gunicorn sda.wsgi -w 4 --threads 2 --bind 0.0.0.0

