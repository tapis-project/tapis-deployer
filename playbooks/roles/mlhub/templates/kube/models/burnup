#!/bin/bash

set -e

here=`pwd`
nfsServerIp=$(kubectl get service nfs-server-service -o jsonpath='{.spec.clusterIP}')
nfsServerIpTemplate="** NFS_SERVER_COMPONENT_IP **"

sed -i.bak "s|${nfsServerIpTemplate}|${nfsServerIp}|g" "$here/deployment.yaml"
rm "$here/deployment.yaml.bak"

kubectl apply -f "$here/service.yaml" \
    -f "$here/deployment.yaml"
