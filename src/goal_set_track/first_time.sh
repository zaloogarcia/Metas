rm db.sqlite3;
rm -r gst/migrations;
python manage.py makemigrations;
python manage.py migrate;
python manage.py migrate --run-syncdb;
python manage.py createsuperuser;
