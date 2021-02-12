#!/bin/bash
./scripts/download_models.sh
python -m pip install -r requirements-extra.txt
python manage.py collectstatic --no-input
python manage.py migrate
exec "$@"
