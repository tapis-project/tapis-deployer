#!/bin/bash

SCRIPT_DIR=$(dirname $0)
TENANT=dev

echo Checking to make sure HTTPie is installed 
HTTPIE_VERSION=$(http --version)
if [[ $? -eq 0 ]]  ; then 
  echo "Found HTTPie version ${HTTPIE_VERSION}"
else
  echo "HTTPie not found - Command 'http --version' failed"
  exit 1
fi

TOKEN=$(${SCRIPT_DIR}/getToken.sh --tenant dev --username testuser2)

if [[ $? -ne 0 ]]  ; then 
  echo "Error getting token."
  exit 1
fi

if [[ -z ${TOKEN} ]] ; then
  echo "Unable to find token file"
  return 1;
else
  echo setting AUTH and CAUTH environment variables with token
  export AUTH=X-Tapis-Token:${TOKEN}
  export CAUTH="-H X-Tapis-Token:${TOKEN}"
fi

echo "Creating systems"
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/ssh-1.json 
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/ssh-2.json 
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/irods-1.json 
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/minio-1.json 
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/minio-2.json 
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems $AUTH < ${SCRIPT_DIR}/../jsonFiles/slurm-1.json 

echo "Adding credentials"
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-ssh-1/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/ssh-creds.json
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-ssh-2/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/ssh-creds.json
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-irods-1/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/irods-creds.json
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-minio-1/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/minio-creds.json
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-minio-2/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/minio-creds.json
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/systems/credential/tapisv3-slurm-1/user/testuser2?skipCredentialCheck=true $AUTH  < ${SCRIPT_DIR}/../jsonFiles/slurm-creds.json

echo "Creating example app"
http POST https://${TENANT}.{{ global_tapis_domain }}/v3/apps $AUTH  < ${SCRIPT_DIR}/../jsonFiles/exampleApp1.json
