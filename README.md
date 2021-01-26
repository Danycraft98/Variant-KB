# Variant-KB

A Variant-KB app, Gene and variant database web application.
The application can easily be deployed to Heroku.
Check out the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) for information about heroku deployment.

## Running Locally

Make sure you have Python 3.9.1 and mysql installed. Also, you must comment out all "django_heroku" in setting.py (there should be two lines)

```sh
$ git clone https://github.com/Danycraft98/Variant-KB.git
$ cd Variant-KB

$ python3 -m venv variant-kb
$ pip install -r requirements.txt

$ mysql -u <username> -p
$ <password>
$ create database variant_db;

$ python manage.py migrate
$ python manage.py runserver
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

 To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
$ heroku create variant-kb
$ git push heroku main
$ heroku open
```

or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
