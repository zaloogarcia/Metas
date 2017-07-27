# Installation process:

1. Verify Python in installed (version 2.7 required) (e.g. `$ python -V`).
2. Install Django using `pip`:
  - `$ pip install django`
3. On file `crontask` replace `$PWD` with the current working directory and save the file,
4. Setup reminders:
  - `$ crontab crontask`
5. Run `$ bash first_time.sh`. You will be prompted to introduce a user name and password for yourself.
6. Run `$ python manage.py runserver` to start running on localhost. Check everything works with your favorite browser.
7. Users created with the command line won't have the default 'Goals' category, create it for yourself.
