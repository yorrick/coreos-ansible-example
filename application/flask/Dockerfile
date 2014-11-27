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

# Set the default directory where CMD will execute
WORKDIR /application


# Install config.py.template file
ADD config.py.template /etc/confd/templates/config.py.template

# Install toml config
ADD flask.toml /etc/confd/conf.d/flask.toml


# prepare files
RUN touch /application/uwsgi_reload
RUN chmod +x /application/confd-watch

# Get pip to download and install requirements:
RUN pip install -r /application/requirements.txt

# Expose ports
EXPOSE 8000
