#!/bin/sh
set -e

# Waiting for database accessibility
echo "⏳  Waiting for Postgres ..."
for i in $(seq 1 30); do
  nc -z db 5432 && break
  sleep 2
done

# Migrations
echo "⚙️   Running migrations …"
python manage.py migrate --noinput

# Colecting static
echo "📦  Collecting static files …"
python manage.py collectstatic --noinput

# Loading data from fixtures
echo "    Loading fixtures ..."
python manage.py loaddata categories_fixture.json products_fixture.json && \

#Clearing cache
python manage.py shell_plus --quiet-load -c \
  "cache.clear(); print('🧹  Cache cleared')"


# Gunicorn
echo "🚀  Starting Gunicorn …"
exec gunicorn store.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers 4 \
      --log-level info \
      --access-logfile - \
      --error-logfile -
