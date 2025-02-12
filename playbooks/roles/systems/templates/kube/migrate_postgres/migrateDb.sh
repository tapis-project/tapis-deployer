#!/bin/bash
#set -xv

# Set properties needed for migration
. ./migrate.env
# Example settings
#export DATABASE_NAME=tapissysdb
#export FROM_ADMIN_USER=postgres
#export ADMIN_PASSWORD=****
#export SERVICE_USER=tapis_sys
#export USER_PASSWORD=****
#export FROM_PG_CONTAINER=deploy/systems-postgres
#export TO_PG_CONTAINER=deploy/systems-postgres-16
#export PG_SCHEMA=tapis_sys

# assume new container has same admin user (change if not)
export TO_ADMIN_USER=${FROM_ADMIN_USER}

#export ENV=DOCKER
export ENV=KUBERNETES


function getTableCounts() {
  CNT_CONTAINER=$1;
  CNT_ADMIN_USER=$2;
  CNT_OUTPUT_FILE=$3;
  CNT_TABLENAME_QUERY="select table_name from information_schema.tables where table_schema = '${PG_SCHEMA}' and table_type = 'BASE TABLE' order by table_name;"

  if [[ ${ENV} == "DOCKER" ]] ; then 
    CNT_PG_TABLES=$(docker exec -i ${CNT_CONTAINER} psql --username ${CNT_ADMIN_USER} ${DATABASE_NAME} -tc "${CNT_TABLENAME_QUERY}")
  elif [[ ${ENV} == "KUBERNETES" ]] ; then 
    CNT_PG_TABLES=$(kubectl exec -i ${CNT_CONTAINER} -- psql --username ${CNT_ADMIN_USER} ${DATABASE_NAME} -tc "${CNT_TABLENAME_QUERY}") 
  fi

  for CNT_TABLE in ${CNT_PG_TABLES} ; do 
    CNT_COUNT_QUERY="select count (*) from ${PG_SCHEMA}.${CNT_TABLE}"
  
    if [[ ${ENV} == "DOCKER" ]] ; then 
      docker exec -i ${CNT_CONTAINER} psql --username ${CNT_ADMIN_USER} ${DATABASE_NAME} -c "${CNT_COUNT_QUERY}"  >> ${CNT_OUTPUT_FILE}
    elif [[ ${ENV} == "KUBERNETES" ]] ; then 
      kubectl exec -i ${CNT_CONTAINER} -- psql --username ${CNT_ADMIN_USER} ${DATABASE_NAME} -c "${CNT_COUNT_QUERY}"  >> ${CNT_OUTPUT_FILE}
    fi
  done;
}

BEFORE_MIGRATE_FILE=$(mktemp /tmp/before-pg-migrate.XXXXX)
AFTER_MIGRATE_FILE=$(mktemp /tmp/after-pg-migrate.XXXXX)
trap 'echo removing temp files && rm "${BEFORE_MIGRATE_FILE}" && rm "${AFTER_MIGRATE_FILE}"' EXIT

getTableCounts ${FROM_PG_CONTAINER} ${FROM_ADMIN_USER} ${BEFORE_MIGRATE_FILE}

  if [[ ${ENV} == "DOCKER" ]] ; then 
    docker exec -i ${FROM_PG_CONTAINER} pg_dumpall --no-password --no-role-passwords --username ${FROM_ADMIN_USER} -l ${DATABASE_NAME} | docker exec -i ${TO_PG_CONTAINER} psql --username ${TO_ADMIN_USER} 
    docker exec -i ${TO_PG_CONTAINER} psql --username ${TO_ADMIN_USER} ${DATABASE_NAME} -c "alter user ${TO_ADMIN_USER} with password '${ADMIN_PASSWORD}'"
    docker exec -i ${TO_PG_CONTAINER} psql --username ${TO_ADMIN_USER} ${DATABASE_NAME} -c "alter user ${SERVICE_USER} with password '${USER_PASSWORD}'"
  elif [[ ${ENV} == "KUBERNETES" ]] ; then 
    kubectl exec -i ${FROM_PG_CONTAINER} -- pg_dumpall --no-password --no-role-passwords --username ${FROM_ADMIN_USER} -l ${DATABASE_NAME} | kubectl exec -i ${TO_PG_CONTAINER} -- psql --username ${TO_ADMIN_USER} 
    kubectl exec -i ${TO_PG_CONTAINER} -- psql --username ${TO_ADMIN_USER} ${DATABASE_NAME} -c "alter user ${TO_ADMIN_USER} with password '${ADMIN_PASSWORD}'"
    kubectl exec -i ${TO_PG_CONTAINER} -- psql --username ${TO_ADMIN_USER} ${DATABASE_NAME} -c "alter user ${SERVICE_USER} with password '${USER_PASSWORD}'"
  fi

getTableCounts ${TO_PG_CONTAINER} ${TO_ADMIN_USER} ${AFTER_MIGRATE_FILE}

echo "=+++++++++++++++++= cat before count  =+++++++++++++++++="
cat ${BEFORE_MIGRATE_FILE} 
echo "=+++++++++++++++++= cat after count  =++++++++++++++++++="
cat ${AFTER_MIGRATE_FILE}
echo "=++++++++++++++++++++= count diffs =++++++++++++++++++++="
echo diff ${BEFORE_MIGRATE_FILE} ${AFTER_MIGRATE_FILE}
diff ${BEFORE_MIGRATE_FILE} ${AFTER_MIGRATE_FILE}
echo "=++++++++++++++++++++= count diffs =++++++++++++++++++++="
