# Jobs Postgres instance

# database

Spin up your postgres database and pgadmin

    cd postgres
    ./burnup

Get pgadmin port:

    kubectl get services | grep pgadmin
    jobs-pgadmin        ClusterIP   10.104.169.241   <none>        80:3XXXX/TCP                                                  6m15s

Point at your kube node with that 3#### port. Login username is `wow@example.com` and password is whatever you set in tapis-jobs-secrets. Once logged in, new connection, host is `jobs-postgres`, username `postgres`, password from sk-secrets.

# Job RabbitMQ

Spin up your postgres database and pgadmin

    cd rabbitmq
    ./burnup
    
Get the administrative port:

    kubectl get services | grep jobs-rabbitmq-mgmt
    jobs-rabbitmq-mgmt       ClusterIP   10.106.18.10     <none>        15672:32037/TCP      2d4h

    In your browser, go to:  http://mykube.example.com:32037
                             Enter credentials for either tapis or jobs user
                               - keys are in Kubernetes tapis-jobs-secrets

# api

Spin up the api

    cd api
    ./burnup

Check what ports you're running on:

    kubectl get services | grep ^sk
    jobs-api            ClusterIP   10.109.23.234    <none>        8000:32544/TCP,8080:32169/TCP,8443:32764/TCP,6157:32408/TCP   14m
    jobs-pgadmin        ClusterIP   10.96.151.188    <none>        80:3XXXX/TCP                                                  28m
    jobs-postgres       ClusterIP   10.108.242.217   <none>        5432/TCP                                                      28m





