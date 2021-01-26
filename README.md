# Variant-KB

A Variant-KB app, Gene and variant database web application.
The application can easily be deployed to Heroku.
Check out the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) for information about heroku deployment.

## Running Locally

Make sure you have Python 3.9.1. To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/Danycraft98/Variant-KB.git
$ cd Variant-KB

$ python3 -m venv variant-kb
$ pip install -r requirements.txt

$ createdb variant_db

$ python manage.py migrate

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
