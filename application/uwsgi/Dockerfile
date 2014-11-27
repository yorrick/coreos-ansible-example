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
RUN curl -L https://github.com/kelseyhightower/confd/releases/download/v0.6.3/confd-0.6.3-linux-amd64 -o /usr/local/bin/confd
RUN chmod +x /usr/local/bin/confd
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

# Install uwsgi server
RUN pip install uwsgi
