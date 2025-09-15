# Tapis Apps component

This directory contains kubernetes deployment files for the Tapis Apps service.
 
Apps passwords are injected into k8s by the Security kernel.
* Secret name is *tapis-apps-secret*
* Keys are *service-password* *postgres-password* *pgadmin-password*
* Service picks up passwords from the env (see api.yml) 

## Database

To start up postgres and pgadmin:
```
  cd postgres
  ./burnup
```

To find pgadmin port:
```
    kubectl get services | grep apps-pgadmin
    apps-pgadmin        ClusterIP    10.102.160.197   <none>        80:30031/TCP
```
 
Pgadmin available at http://mykube.example.com:30031

Pgadmin username is wow@example.com 

Pgadmin password from apps-secrets:
```
 k get secret tapis-apps-secrets -o json | jq -r '.data."pgadmin-password"' | base64 -d
```

To create Server in pgadmin use:
```
  Host: apps-postgres
  Username: postgres
  Password: *tapis-apps-secrets : postgres-password*
```

## Service

Service password from apps-secrets: 
```
 k get secret tapis-apps-secrets -o json | jq -r '.data."service-password"' | base64 -d 
```

To start apps service 
```
  cd api 
  ./burnup 
```

To see all apps artifacts: 
```
  k get all | grep apps 
```

## To allow for attaching to jvm with debugger

NOTE: Work in progress, not yet successful

Make sure pod is running with a jvm debug port available.
Label the pod so the debug service can find it.
```
k label pod/apps-api-9d7456fc6-26wrf podname=apps-api-debug
```

Create a service which will expose the debug port (8000) as a ClusterIP
```
k create -f api/service_debug.yml
```

Determine port for debugger, e.g.
```
k get all | grep apps-api-debug
service/apps-api-debug        ClusterIP    10.96.180.48     <none>        8000:32066/TCP      42s
```

jvm debugger should be able to attach to http://mykube.example.com:32066

BUT currently this results in "connection refused"

Could also try port forwarding, e.g. on cic02 do
```
k port-forward pod/apps-api-57bcdf9769-9jrsp 8000:8000
```

and then use ssh port forwarding when connecting from localhost to cic02.

BUT this results in "connection reset"
