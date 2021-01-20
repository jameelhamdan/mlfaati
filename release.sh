#!/bin/bash
python -m pip install -r requirements-extra.txt
python manage.py collectstatic --no-input
python manage.py migrate
exec "$@"
