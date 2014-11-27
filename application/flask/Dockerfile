############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM yorrick/uwsgi

# File Author / Maintainer
MAINTAINER Yorrick Jansen

# Copy the application folder inside the container
ADD . /application

# prepare files
RUN touch /application/uwsgi_reload
RUN chmod +x /application/confd-watch

# Get pip to download and install requirements:
RUN pip install -r /application/requirements.txt

# Expose ports
EXPOSE 8000

# Set the default directory where CMD will execute
WORKDIR /application

# CMD python server.py
# CMD uwsgi --http 0.0.0.0:8000 --master --module app --callable app --touch-reload /application/uwsgi_reload --logto /var/log/application.log

