#!/bin/bash
#
# Exit on error
ECHO "START BUILD"
set -e

# Navigate to the directory containing your Django project
cd path/to/your/django/project

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start your application (this is for illustration; in production, you would use a server like Gunicorn)
python manage.py runserver 0.0.0.0:8000
ECHO "END BUILD"
ECHO "END BUILD"
