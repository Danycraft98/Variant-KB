FROM ubuntu

WORKDIR /code

# Update the sources list
RUN apt-get update \
 && apt-get update -y \
 && apt-get install -y python3-pip python3-dev \
 && cd /usr/local/bin \
 && ln -s /usr/bin/python3 python \
 && pip3 install --upgrade pip \
 && apt-get install -y libmysqlclient-dev \
 && apt-get install -y libpango1.0-0 \ 
 && apt-get install -y libcairo2 \
 && apt-get install -y libpq-dev

# Configure the python requirements
COPY . /srv/variant_db/server/
WORKDIR /srv/variant_db/server

ADD requirements.txt /code/
RUN pip3 install -r requirements.txt

ADD /static .

CMD ["python", "manage.py", "migrate"]
CMD ["python", "populate_db.py"]
CMD ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]