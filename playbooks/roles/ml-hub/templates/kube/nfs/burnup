#!/bin/bash

set -e

here=`pwd`

kubectl apply -f "$here/service.yaml" \
    -f "$here/pvc.yaml" \
    -f "$here/deployment.yaml" \
    