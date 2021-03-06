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
export FLEETCTL_TUNNEL=127.0.0.1:$VAGRANT_SSH_PORT

# Cleanup known_hosts file 
echo '' > /Users/yorrick/.fleetctl/known_hosts

# tunnel configuration can b found using "vagrant ssh-config core-01" by example
fleetctl list-machines
fleetctl submit services/*
fleetctl list-unit-files

fleetctl start database.service
fleetctl start database-discovery.service
fleetctl start application@1.service
fleetctl start application@2.service

# get unit statuses
fleetctl status database.service
fleetctl status application@1
fleetctl list-units
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

## Build and push application image
```
docker build -t yorrick/application /home/core/share/application/flask && docker push yorrick/application
```

## Build and push database image
```
docker build -t yorrick/database /home/core/share/application/database && docker push yorrick/database
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



## Debug confd 
```
docker run --name application-test --rm -t -i yorrick/application /bin/bash  # run container
confd -onetime=true -debug=true -node 172.17.42.1:4001  # launch confd manually
```


## Backup database files (please shut down the database before doing that!)
```
# on your host, run
fleetctl stop database.service


# run this on node that runs the database
sudo docker run -it --rm --volumes-from database-01 -v /home/core/share:/backup --name dbdata ubuntu tar cvf /backup/backup.tar /etc/postgresql /var/log/postgresql /var/lib/postgresql

# or, using fleetctl
fleetctl stop database.service

rm backup.tar
fleetctl destroy database-backup.service
fleetctl start services/database-backup.service
fleetctl status database-backup.service
fleetctl start database.service


fleetctl stop database.service
fleetctl destroy database-restore.service
fleetctl start services/database-restore.service
fleetctl status database-restore.service
fleetctl start database.service
```



Test that you can connect to postgres from container
psql --username docker --host 172.12.8.101 --port 5432 docker

To initialize database, inside application container in ipython, run
from database import db
db.create_all()






