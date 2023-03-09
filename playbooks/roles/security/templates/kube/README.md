# Security Kernel Postgres instance

## 1-time prep

Create a file called ~/sk-secrets something like this: 

    #!/bin/bash
    kubectl create secret generic sk-postgres-secrets \
    --from-literal=sk-postgres-password=changeme123 \
    --from-literal=sk-pgadmin-password=changeme456
    
A good way to generate those passwords is:

    openssl rand -hex 16


# database

Spin up your postgres database and pgadmin

    cd postgres
    ./burnup

Get pgadmin port:

    kubectl get services | grep pgadmin
    sk-pgadmin        NodePort    10.104.169.241   <none>        80:31348/TCP                                                  6m15s

Point at your kube node with that 3#### port. Login username is `wow@example.com` and password is whatever you set in ~/sk-secrets. Once logged in, new connection, host is `sk-postgres`, username `postgres`, password from sk-secrets.

# api

Spin up the api

    cd api
    ./burnup

Check what ports you're running on:

    kubectl get services | grep ^sk
    sk-api            NodePort    10.109.23.234    <none>        8000:32544/TCP,8080:32169/TCP,8443:32764/TCP,6157:32408/TCP   14m
    sk-pgadmin        NodePort    10.96.151.188    <none>        80:32119/TCP                                                  28m
    sk-postgres       NodePort    10.108.242.217   <none>        5432/TCP                                                      28m





