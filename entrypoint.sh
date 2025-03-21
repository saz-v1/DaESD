#!/bin/bash

# Make sure media directory exists with correct permissions
mkdir -p /app/media/community_images
chmod -R 777 /app/media

# Run migrations first
python manage.py migrate

# Start the Django server
python manage.py runserver 0.0.0.0:8000
