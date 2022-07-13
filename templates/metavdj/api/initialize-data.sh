#!/bin/bash

# assign permissions for streams admin and meta admin on db and root

SRVCTOKEN=`cat ~/metadata-service-token`

DB=StreamsDevDB
debugport=`kubectl get service restheart-debug  -o json | jq .spec.ports[0].nodePort -r`

echo "The environment determines Streams DB naming, so we set it here $DB"

echo ""; echo "point1"
echo "create db - currently init with Streams db per environment since they need startup access"
curl -s -X PUT http://c006.rodeo.tacc.utexas.edu:$debugport/$DB


echo ""; echo "point2"
echo "assign permissions for meta admin on root"
# SK grant permissions for a meta to all operations at MongoDB root
token="X-Tapis-Token: $SRVCTOKEN"
user="X-Tapis-User: meta"
tenant="X-Tapis-Tenant: admin"
content="Content-Type: application/json"
data="{'user':'meta','tenant':'admin','permSpec':'meta:admin:GET,POST,PUT,PATCH,DELETE:*:*:*'}"

curl -s -X POST -H "$token" -H "$user" -H "$tenant" -H "$content" -d "$data" https://dev.develop.tapis.io/v3/security/user/grantUserPermission?tenant=admin

########

echo ""; echo "point3"
echo "assign permissions for streams admin on $DB "
# SK grant permission for a service streams with all operations
user="X-Tapis-User: meta"
data="{'user':'streams','tenant':'admin','permSpec':'meta:admin:GET,POST,PUT,PATCH,DELETE:StreamsDevDB:*:*'}"

curl -s -X POST -H "$token" -H "$user" -H "$tenant" -H "$content" -d "$data" https://dev.develop.tapis.io/v3/security/user/grantUserPermission?tenant=admin

echo ""
echo "Adding the collections for $DB "
curl -s -X PUT -H "$token" -H "$user" -H "$tenant" -H "$content" https://dev.develop.tapis.io/v3/meta/$DB/streams_instrument_index
curl -s -X PUT -H "$token" -H "$user" -H "$tenant" -H "$content" https://dev.develop.tapis.io/v3/meta/$DB/streams_project_metadata
curl -s -X PUT -H "$token" -H "$user" -H "$tenant" -H "$content" https://dev.develop.tapis.io/v3/meta/$DB/streams_alerts_metadata
curl -s -X PUT -H "$token" -H "$user" -H "$tenant" -H "$content" https://dev.develop.tapis.io/v3/meta/$DB/streams_templates_metadata
curl -s -X PUT -H "$token" -H "$user" -H "$tenant" -H "$content" https://dev.develop.tapis.io/v3/meta/$DB/streams_channel_metadata
