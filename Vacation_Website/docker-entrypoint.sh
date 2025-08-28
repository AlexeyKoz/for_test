#!/bin/bash

# Django Docker entrypoint script

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up - executing command"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create default superuser if no admin exists
echo "Checking for admin users..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
admin_count = User.objects.filter(is_staff=True).count()
if admin_count == 0:
    # Create default admin only if no admin users exist
    User.objects.create_superuser(email='admin@example.com', password='admin123', first_name='Default', last_name='Admin')
    print('✅ Default admin created: admin@example.com / admin123')
    print('💡 You can create additional admin users with:')
    print('   python manage.py create_dashboard_admin')
else:
    print(f'✅ Found {admin_count} admin user(s) in database')
    for user in User.objects.filter(is_staff=True)[:3]:
        print(f'   - {user.email} ({user.first_name} {user.last_name})')
    if admin_count > 3:
        print(f'   ... and {admin_count - 3} more')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Populate database if needed (run your populate_db command)
echo "Populating database..."
python manage.py populate_db || echo "Database population command not found or failed"

# Start the Django development server or gunicorn
echo "Starting Django application..."
if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
fi
