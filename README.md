# Variant-KB -- Server Configuration (Everything You Need)

The following repository contains all files required to spin up the Variant-DB web-app on UHN servers. As of writing this readme, currently Ian's lab will
be using the web-app. The Variant-KB web-app helps store and access Genes and Variants as well as their relevant information. The web-app is python based (python 3.9.1) and uses Django as the main framework. You can view the demo [here](https://variant-kb.herokuapp.com/)<br/>

The application can easily be deployed to Heroku, which you can find more informations at [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python).

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

$ mysql -u <username> -p variant_db < variant_db_<latestschemadate>.sql
$ <password>
```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## Deploying to Heroku

To deploy to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
$ heroku create variant-kb
$ git push heroku main
$ heroku open
```

## Deploying with Dockerfile

The ```Dockerfile``` uses Python as its base operating system. Also, ```RUN pip3 install --upgrade pip && pip3 install -r requirements.txt``` upgrades the pip3 and installs all that is required to run the app automatically.

```
###############################################################################
## Dockerfile to build the Variant server running the Variant-KB Web App
###############################################################################
FROM python:3.9.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . /code/
```

### Server Updates
After pushing updates to gitlab, the following commands can be used to access
the web-app server and any related servers (database).

### OTP
Go to [UHN Remote](http://www.uhnresearch.ca/remote) and otp into the servers.

### Server SSH
Assuming you have access to Mordor and the following nodes (if not speak to Zhibin) do the following:

```
$ ssh -p 10022 <account>@192.168.198.99 
$ ssh -p 10025 <account>@node12
$ mysql -u <username> -p
$ <password>
```

### Updating The Server

Here is a very systematic method of updating the server after pulling from gitlab (must update docker image and container for the server):
```
$ docker ps -a
$ 
$ docker stop <container ID>
$ docker rm <container ID>
$ docker run -d -e SQL_USER="<user>" -e SQL_PASSWORD="<password>" -p 0.0.0.0:8000:8005 ?
```

Make sure to find the container ID of the rk_lims_image container.

### Useful Commands

Create Migration files<br/>
`$ Python manage.py makemigrations`

Load Migrations (Make sure the database is created before executing the command)<br/>
`$ Python manage.py migrate`

Create Super User<br/>
`$ Python manage.py createsuperuser`

### Server Database Schema Import
From local to Mordor:<br/>
`$ scp -P 10022 variant_db_<latest_schema_date>.sql <username>@192.168.198.99:/mnt/work1/users/home/<username>`

From Mordor to database server:<br/>
`$ scp -P 10022 /mnt/work1/users/home/<username>/variant_db_<latest_schema_date>.sql <username>@node12:/home/<username>`

Updating the database:<br/>
`$ mysql -u <username> -p variant_db < variant_db_<latest_schema_date>.sql`
