### hammock/mpackard 20210616


# Script to add Monitoring read only access for Apps service DB using psql
# user and grant read only acces
# Postgres password must be set in env var MONITOR_PASSWORD

function get_pw() {
  echo $(kubectl get secret ${1} -o jsonpath={.data.postgres-password} | base64 -d)
}

# Apps
MONITOR_PASSWORD=$(get_pw tapis-apps-secrets)
DB_HOST=$(kubectl get service apps-postgres -o jsonpath={.spec.clusterIP})
DB_USER='postgres'

if [ -z "${MONITOR_PASSWORD}" ]; then
  echo "Please set env var MONITOR_PASSWORD before running this script"
  exit 1
fi

./venv/bin/pgcli --host=${DB_HOST} --username=${DB_USER} --dbname=${DB_NAME} show tables

## # Run sql to create user if it does not exist
## psql --host=${DB_HOST} --username=${DB_USER} --dbname=${DB_NAME} -q << EOB
## -- Create user if it does not exist
## DO \$\$
## BEGIN
##   CREATE ROLE monitor WITH LOGIN;
##   EXCEPTION WHEN DUPLICATE_OBJECT THEN
##   RAISE NOTICE 'User already exists. User name: monitor';
## END
## \$\$;
## ALTER USER monitor WITH ENCRYPTED PASSWORD '${MONITOR_PASSWORD}';
## GRANT SELECT ON ALL TABLES IN SCHEMA tapis_app TO monitor;
## GRANT CONNECT ON DATABASE tapisappdb TO monitor;
## GRANT USAGE ON SCHEMA tapis_app TO monitor;
## 
## EOB
## 
