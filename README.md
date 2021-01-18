# Variant-DB -- Server Configuration (Everything You Need)
The following repository contains all files required to spin up the Variant DB 
web-app on UHN servers. As of writing this readme, currently Ian's lab will
be using the web-app. The web-app helps store and access gene and variant as well as their
relevant information. The web-app is python based (python 3.7) and uses django
as a web framework.

## Dockerfile
The ```Dockerfile``` uses Python3 as its base operating system. Notice that --dbhost is
specified when running main.py, which links the web-app container to the
a maria-DB database containing all relevant data, within Mordor (more on that 
later). Also, ```RUN pip3 install -r requirements.txt``` installs all that is
required to run the app automatically.

```
###############################################################################
## Dockerfile to build the LIMS-Reagent server running the LIMS-Reagent DB Web App
###############################################################################
FROM python:3.9.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
```

## Local Development (Setup)
Make sure you are using ```Python 3``` (3.9) and ```pip3``` to be able to run
the app. You can always refer to the Dockerfile to see if you are missing
anything (if the app doesn't want to boot up).

### Requirements.txt
You can find all the pip3 install requirements in requirements.txt file.
Subsequently, you don't need to go theough them individually, you should be able
to just:

``` Before installing, make sure python3 is installed and pip3 is available.```

``` INSTALL MYSQL PRIOR TO RUNNING THE REQUIREMENTS INSTALL ```

```
$ brew install mysql
```

```
$ pip3 install -r requirements.txt
```

``` If you get an egg_info error try upgrating setuptools ```

```
$ pip3 install --upgrade setuptools
```

on your local machine. The apt-get source list updates found in the Dockerfile
will need to be done prior to running the mentioned command (unless you already
have everything) as well.

## Local Machine Configuration
### MySQL Configuration

Before starting the application for the first time you must start the server:

```
$ mysql.server start
```

Open MySQL (password is nothing so just hit enter):

```
$ mysql -u irene -p
```

Create the reagent_db Database:

```
$ CREATE DATABASE variant_db;
```

Exit out of MySQL and go into the reagent_db folder containing the latest .sql file
and run:

```
$ mysql -u irene -p variant_db < variant_db_<latestschemadate>.sql
```

Anytime after this, only the ``` $ mysql.server start ``` command will be
necessary to run the application (unless you need to update the database from
a pull request with a new schema)

# Server Updates
After pushing updates to gitlab, the following commands can be used to access
the web-app server and any related servers (database).

## OTP
Go to ```http://www.uhnresearch.ca/remote``` and otp into the servers.

## Server SSH
Assuming you have access to Mordor and the following nodes (if not speak to
Zhibin) do the following:

```
$ ssh -p 5059 <account>@192.75.165.28
```

### Reagents-DB Server
```
$ ssh -p 10025 <account>@node12
```
```
$ cd /home/irene/variant-db
```

Now you can pull ad update the server.

### Database Server
```
$ ssh -p 10022 <account>@node12
```
```
$ cd /home/irene
```

Here you have can run (Ask Richard for permissions):

```
$ mysql -u root -p
```

## Updating The Server
### Docker
Here is a very systematic method of updating the server after pulling from
gitlab (must update docker image and container for the server):

```
$ docker ps -a
```

Find the container ID of the rk_lims_image container.


```
$ docker stop <container ID>
```
```
$ docker rm <container ID>
```
```
$ docker run -d -e SQL_USER="<user>" -e SQL_PASSWORD="<password>" -p 0.0.0.0:5000:5005 flaskapp
```
```
$ docker run -d -e SQL_USER="irene" -e SQL_PASSWORD="irene123" -p 0.0.0.0:5000:5005 flaskapp
```

## Useful Commands

### Django Commands

Create Migration files

```
Python manage.py makemigrations
```

Load Migrations (Make sure the database is created before executing the command)


```
Python manage.py migrate
```

Create Super User


```
Python manage.py createsuperuser
```

### Server Database Schema Import

From local to Mordor:

```
scp -P 5059 reagent_lims_<latest_schema_date>.sql <username>@192.75.165.28:/mnt/work1/users/home/<username>
```

From Mordor to database server:

```
scp -P 10022 /mnt/work1/users/home/<username>/reagent_db_<latest_schema_date>.sql <username>@node12:/home/<username>
```

Updating the database:

```
mysql -u <username> -p reagent_db < reagent_db_<latest_schema_date>.sql
```
