#1/usr/bin/env sh

echo "Migrations"
python3 manage.py migrate --noinput

echo "Run server"
python3 manage.py runserver 0.0.0.0:8001