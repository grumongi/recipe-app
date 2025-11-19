#!/bin/bash

# Production deployment script for Recipe App

echo "Starting production deployment..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "Deployment script completed!"