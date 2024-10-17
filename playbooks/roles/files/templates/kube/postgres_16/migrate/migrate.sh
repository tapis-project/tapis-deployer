#!/bin/bash

#setup migration configmap, and get some things out of it
kubectl create -f files-migrate-pg-11-to-16-vars-configmap.yml
POSTGRES_11_POD=$(kubectl get configmap files-migrate-pg-11-to-16-vars-configmap -o jsonpath="{.data.PG_11_POD}")
POSTGRES_16_POD=$(kubectl get configmap files-migrate-pg-11-to-16-vars-configmap -o jsonpath="{.data.PG_16_POD}")
POSTGRES_16_ADMIN_USER=$(kubectl get configmap files-migrate-pg-11-to-16-vars-configmap -o jsonpath="{.data.PG_16_ADMIN_USER}")
POSTGRES_16_ADMIN_USER_PASSWORD=$(kubectl get secrets tapis-files-secrets -o jsonpath="{.data.postgres-password}" | base64 -d)

if [[ -z ${POSTGRES_11_POD} ]] ; then
    echo "ERROR:  Unable to determine postgres 11 pod name."
fi

if [[ -z ${POSTGRES_16_POD} ]] ; then
    echo "ERROR:  Unable to determine postgres 16 pod name."
fi

#bring up postgres 16
kubectl apply -f ../service.yml 
kubectl apply -f ../pg-16-pvc.yml 
kubectl apply -f ../deploy.yml 
kubectl wait --for=condition=available deploy/files-postgres-16

#the container should be up, but give a moment for postgres to start
sleep 2

# migrate the data
kubectl create configmap files-migrate-pg-11-to-16-sh-configmap --from-file files-migrate-pg-11-to-16-sh-configmap
kubectl create -f files-migrate-pg-11-to-16.yml
kubectl wait --for=condition=complete job/files-migrate-pg-11-to-16

kubectl logs jobs.batch/files-migrate-pg-11-to-16

# set passwords
PSQL_COMMAND="alter user ${POSTGRES_16_ADMIN_USER} with password '${POSTGRES_16_ADMIN_USER_PASSWORD}'"
kubectl exec -it deploy/${POSTGRES_16_POD} -- psql -U ${POSTGRES_16_ADMIN_USER} -tc "${PSQL_COMMAND}"

# check db/table counts
kubectl create -f files-migrate-check-pg-11-to-16.yml
kubectl wait --timeout=120s --for=condition=complete job/files-migrate-check-pg-11-to-16

kubectl logs jobs.batch/files-migrate-check-pg-11-to-16

#cleanup all migration related containers, and bring down postgres 16
kubectl delete configmap files-migrate-pg-11-to-16-sh-configmap
kubectl delete configmap files-migrate-pg-11-to-16-vars-configmap
kubectl delete -f files-migrate-pg-11-to-16.yml
kubectl delete -f files-migrate-check-pg-11-to-16.yml
kubectl delete -f ../service.yml
kubectl delete -f ../deploy.yml

# leave the pvc in-tact ... uncomment the line below to blow away the data
#kubectl delete -f ../pg-16-pvc.yml 
