#!/bin/bash

set -e

here=`pwd`
nfsServerIp=$(kubectl get service mlhub-nfs-server-service -o jsonpath='{.spec.clusterIP}')
nfsServerIpTemplate="{{ NFS_SERVER_COMPONENT_IP }}"

sed -i.bak "s|${nfsServerIp}|${nfsServerIpTemplate}|g" "$here/deployment.yaml"
rm "$here/deployment.yaml.bak"

kubectl delete -f "$here/deployment.yaml"