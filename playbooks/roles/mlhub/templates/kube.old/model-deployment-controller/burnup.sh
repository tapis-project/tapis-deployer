#!/bin/bash

set -e

here=`pwd`
nfsServerIp=$(kubectl get service mlhub-nfs-server-service -o jsonpath='{.spec.clusterIP}')
nfsServerIpTemplate="{{ NFS_SERVER_COMPONENT_IP }}"

# Replace the template with the nfs server ip
sed -i.bak "s|${nfsServerIpTemplate}|${nfsServerIp}|g" "$projectDir/deploy/k8s/minikube/model-deployment-controller/deployment.yaml"
rm "$projectDir/deploy/k8s/minikube/model-deployment-controller/deployment.yaml.bak"

kubectl apply -f "$projectDir/deploy/k8s/minikube/tapis-deployment-strategies-cm.yaml"

kubectl apply -f "$projectDir/deploy/k8s/minikube/model-deployment-controller/deployment.yaml"

# Return the manifest back to the template
sed -i.bak "s|${nfsServerIp}|${nfsServerIpTemplate}|g" "$projectDir/deploy/k8s/minikube/model-deployment-controller/deployment.yaml"
rm "$projectDir/deploy/k8s/minikube/model-deployment-controller/deployment.yaml.bak"
