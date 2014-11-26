############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Yorrick Jansen

# Update the sources list
RUN apt-get update
RUN apt-get install curl -y

# Install confd
RUN cd /usr/local/bin
RUN curl -L https://github.com/kelseyhightower/confd/releases/download/v0.6.3/confd-0.6.3-linux-amd64 -o confd
RUN chmod +x confd
RUN mkdir -p /etc/confd/{conf.d,templates}


# Install basic applications
RUN apt-get install -y tar git dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Install postgres clients (for debugging and for psycopg2)
RUN apt-get install -y postgresql-client-9.3 libpq-dev

# install nginx: not for now
# RUN apt-get install -y python-software-properties
# RUN apt-get update
# RUN apt-get install -y nginx


# Copy the application folder inside the container
ADD . /application
RUN touch /application/uwsgi_reload

# Get pip to download and install requirements:
RUN pip install -r /application/requirements.txt
RUN pip install uwsgi

# Expose ports
EXPOSE 8000

# Set the default directory where CMD will execute
WORKDIR /application

# CMD python server.py
CMD uwsgi --http 0.0.0.0:8000 --master --module app --callable app --touch-reload /application/uwsgi_reload

