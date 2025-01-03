#!/bin/bash

echo "Flushing database..." 
echo "yes" | python manage.py flush > /dev/null

echo "Deleting uploaded files"
rm -rf uploaded/*

echo "Deleting old migrations"
rm -rf db.sqlite3
rm -rf ./core/migrations

if [[ "$1" == "--clean" ]]; then
    exit 0;
fi

echo "Starting fresh database migration..."
python manage.py makemigrations
python manage.py makemigrations core
python manage.py migrate

if [[ "$1" == "--seed" ]]; then
    echo "Seeding..."
    python manage.py seed
    echo "Seeding complete"
fi
