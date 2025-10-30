#!/usr/bin/env bash
# exit immediately if a command exits with a non-zero status
set -euo pipefail

echo "==> Installing dependencies"
pip install --upgrade pip  # optional but good
pip install -r requirements.txt

echo "==> Running database migrations"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "==> Collecting static files"
python manage.py collectstatic --noinput

echo "==> Build complete"
