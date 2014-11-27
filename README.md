# CoreOS instructions

1. Install ansible and its dependencies
```
brew install ansible
ansible-galaxy install -r ansible-requirements.txt --ignore-errors --force
```

2. Boot vagrant VMs (provisioning will be made at the same time)
```
vagrant up
```

3. Install fleet and configure it
```
brew install fleetctl
```

4. Submit and run fleet services from your host

```
# Add vagrant private key to ssh (fleetctl doesn’t expose any options to configure the SSH connection)
ssh-add ~/.vagrant.d/insecure_private_key

# Find vagrant ssh port
export VAGRANT_SSH_PORT=`vagrant ssh-config core-01 | grep Port | awk '{print $2}'`

# Cleanup known_hosts file 
echo '' > /Users/yorrick/.fleetctl/known_hosts

# tunnel configuration can b found using "vagrant ssh-config core-01" by example
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT submit services/*
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT start database.service
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT start database-discovery.service
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT start application@1.service
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT start application@2.service

# get unit statuses
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT status database.service
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT status application@1
fleetctl --tunnel 127.0.0.1:$VAGRANT_SSH_PORT list-units
```


### To list services in etcd 
```
curl -L http://127.0.0.1:4001/v2/keys/services  # from coreos 
curl -L http://172.17.42.1:4001/v2/keys/services  # from container
etcdctl ls --recursive /
```




# Build docker containers

On core-01 by example, run

## Build and push base uwsgi image
```
docker build -t yorrick/uwsgi /home/core/share/application/uwsgi && docker push yorrick/uwsgi
```

## Build image and push application image
```
docker build -t yorrick/application /home/core/share/application/flask && docker push yorrick/application
```

## Pull database image
```
docker pull yorrick/database
```


# Tests

## Test if application container boots
```
docker run --rm -t -i --name application-01 -p 80:80 yorrick/application
```

## Run application container in detached mode
```
docker run -d --name application-01 -p 80:80 yorrick/application
```


## Commit a container (to save database state)
```
docker commit database-01 yorrick/database
```


## Debug confd 
```
docker run --name application-test --rm -t -i -p 8000:8000 yorrick/application /bin/bash  # run container
confd -onetime=true -debug=true -node 172.17.42.1:4001  # launch confd manually
```




Rebuild application container
cd share/application/
docker stop application-01; docker rm application-01; docker build -t yorrick/application . && docker run -t -i --name application-01 -p 80:80 yorrick/application /bin/bash
docker push yorrick/application

Test that you can connect to postgres from container
psql --username docker --host 172.12.8.101 --port 5432 docker

To initialize database, inside application container in ipython, run
from database import db
db.create_all()






