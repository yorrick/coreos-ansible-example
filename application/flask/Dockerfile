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
RUN apt-get install nginx curl -y

# Install confd
RUN cd /usr/local/bin
RUN curl -L https://github.com/kelseyhightower/confd/releases/download/v0.6.3/confd-0.6.3-linux-amd64 -o confd
RUN chmod +x confd
RUN mkdir -p /etc/confd/{conf.d,templates}


# Install basic applications
RUN apt-get install -y tar dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Install postgres clients (for debugging and for psycopg2)
RUN apt-get install -y postgresql-client-9.3 libpq-dev

# Copy the application folder inside the container
ADD . /application

# Get pip to download and install requirements:
RUN pip install -r /application/requirements.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /application

# Set the default command to execute    
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python server.py

