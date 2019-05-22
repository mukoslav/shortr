in order to run shortr:

$ git clone https://github.com/mukoslav/shortr.git
$ cd ~/path/to/project/folder
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

create a postgres db and add the credentials to settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

go to localhost:8000 to view the app

to run the tests:
$ python manage.py test shortener/
