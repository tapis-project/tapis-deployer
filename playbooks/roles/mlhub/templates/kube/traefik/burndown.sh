#!/bin/bash

set -e

$here=`pwd`

kubectl delete -f "$here/deployment.yaml" \
    -f "$rootDir/traefik-dynamic-config.yaml"