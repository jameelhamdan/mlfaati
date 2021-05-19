#!/bin/bash
./scripts/download_models.sh
./scripts/build_docs.sh
python -m pip install -r requirements-extra.txt --no-cache-dir
python manage.py collectstatic --no-input
python manage.py migrate
exec "$@"
