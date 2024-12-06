# Changelog 

## 1.8.0

### Breaking Changes for Deployer Admins

- Note that we updated the Hashicorp Vault image by many release steps (1.8.3 to 1.16.3). While this did not cause issues in our testing, please be sure you have a good Vault backup before proceeding with the updagrade.

- The files postgres data must be migrated to the new postgres 16 container before deploying 1.8.0.
  The new version will have a burnup script for a files-postgres-16 container, and
  it uses a new (empty) pvc.  Before bringing all files services up, you must 
  bring up the new files-postgres-16 container, and migrate the postgres data
  from the files-postgres container to the files-postgres-16 container.  The best
  place to get information about this is the postgres docs.  This could be done 
  manually (using dbdump/dbdumpall).  One thing to note is that passwords for
  postgres users will not be migrated and must be reset due to changes in the
  way that postgres hashes the passwords, so be sure to find the db user passwords
  before you get started.  This could be scripted and an example of how that might 
  be done is included.  Here is the information on the examples:
  
  -  Backup your current database in case something goes wrong.
  -  After deployment, burn down all files pods EXCEPT files-postgres. 
  -  Verify that the scripts look correct for your environment.  Check the variables 
     are defined in postgres_16/migrate/files-migrate-pg-11-to-16-vars-configmap.yml
  -  In postgres_16 directory, cd into migrate, and run migrate.sh.
  -  Check table counts after the job completes (these will be located in stdout for 
     the script).  Check for errors, etc.
  -  cd into the files/postgres directory (postgres - not postgres_16), and burndown 
     the old postgres.
  -  Once the data is successfully migrated and verified, burndown any files services 
     that are currently running and restart.  To do this, cd into the files directory 
     and run the burndown and burnup scripts.


### Service Updates

- [Apps: 1.7.0 to 1.8.0 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/dev/CHANGELOG.md)
- [Abaco/Actors: 1.7.0 to 1.8.0 (abaco/core-v3)](https://github.com/TACC/abaco/blob/prod-v3/CHANGELOG.md)
- [Authenticator: 1.7.0 to 1.8.0 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)
- [Files: 1.7.0 to 1.8.0 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Globus-Proxy: 1.7.0 to 1.8.0 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)
- [Jobs: 1.7.0 to 1.8.0 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Meta: 1.7.0 to 1.8.0 (tapis/metaapi, tapis-meta-rh-server)](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
- [Notifications: 1.7.0 to 1.8.0 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
- [Pods: 1.7.0 to 1.8.0 (tapis/pods-api)](https://github.com/tapis-project/pods_service/blob/dev/CHANGELOG.md)
- [Security: 1.7.0 to 1.8.0 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Systems: 1.7.0 to 1.8.0 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
- [Workflows: 1.7.0 to 1.8.0 (tapis/workflows-api, tapis/workflows-pipelines, tapis/workflow-engine-streams)](https://github.com/tapis-project/tapis-workflows/blob/release-1.7.0/CHANGELOG.md)
- [TapisUI: 1.7.0 to 1.8.0 (tapis/tapisui)](https://github.com/tapis-project/tapis-ui/blob/dev/CHANGELOG.md)
- [Vault: 1.8.3 to 1.16.3 (hashicorp/vault:1.16.3)](https://github.com/hashicorp/vault/releases/tag/v1.16.3)


## 1.7.0 

### Service Updates

- [Apps: 1.6.4 to 1.7.0 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/dev/CHANGELOG.md)
- [Authenticator: 1.6.2 to 1.7.0 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)
- [Files: 1.6.4 to 1.7.0 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.6.4 to 1.7.0 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Meta: 1.6.1 to 1.7.0 (tapis/metaapi, tapis-meta-rh-server)](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
- [Notifications: 1.6.2 to 1.7.0 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
- [Security: 1.6.3 to 1.7.0 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Systems: 1.6.5 to 1.7.0 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
- [Globus-Proxy: 1.6.4 to 1.7.0 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
- [Workflows: 1.6.0 to 1.7.0 (tapis/workflows-api, tapis/workflows-pipelines, tapis/workflow-engine-streams)](https://github.com/tapis-project/tapis-workflows/blob/release-1.7.0/CHANGELOG.md)
- [Pods: 1.6.0 to 1.7.0 (tapis/pods-api)](https://github.com/tapis-project/pods_service/blob/dev/CHANGELOG.md)
- [TapisUI: 1.7.0 (tapis/tapisui)](https://github.com/tapis-project/tapis-ui/blob/dev/CHANGELOG.md)

### Breaking Changes for Deployer Admins

- If using the globus-proxy component, you must provide 2 variables in host_vars: `globus_client_id` and `globus_client_secret`. They correspond to the id and secret of the service client, as described here: https://docs.globus.org/guides/recipes/automate-with-service-account/ .


## 1.6.4 

### Service Updates

- [Systems: 1.6.4 to 1.6.5 (tapis/systems)](Systems changes: https://github.com/tapis-project/tapis-systems/blob/1.6.5/CHANGELOG.md)
- [Apps: 1.6.3 to 1.6.4 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.6.4/CHANGELOG.md)
- [Files: 1.6.3 to 1.6.4 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.6.3 to 1.6.4 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Security: 1.6.2 to 1.6.3 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Globus-Proxy: 1.6.2 to 1.6.4 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)

### Breaking Changes for Deployer Admins

- If using the globus-proxy component, you must provide 2 variables in host_vars: `globus_client_id` and `globus_client_secret`. They correspond to the id and secret of the service client, as described here: https://docs.globus.org/guides/recipes/automate-with-service-account/ .


## 1.6.3 

### Service Updates

- [Authenticator: 1.6.1 to 1.6.2 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)
- [Systems: 1.6.2 to 1.6.3 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.6.3/CHANGELOG.md)
- [Files: 1.6.2 to 1.6.3 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.6.2 to 1.6.3 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Globus-Proxy: 1.6.0 to 1.6.2 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)
- Removed Monitoring-Kibana & Monitoring-Elasticsearch components. These may be left in burndown scripts for now but will be removed in a future release.

## 1.6.2

### Service Updates

- [Systems: 1.6.1 to 1.6.2 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.6.2/CHANGELOG.md)
- [Apps: 1.6.1 to 1.6.2 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.6.2/CHANGELOG.md)
- [Notifications: 1.6.1 to 1.6.2 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/1.6.2/CHANGELOG.md)
- [Files: 1.6.1 to 1.6.2 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.6.1 to 1.6.2 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Security: 1.6.1 to 1.6.2 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Meta: 1.6.0 to 1.6.1 (tapis/metaapi, tapis-meta-rh-server)](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
- [Authenticator: 1.6.0 to 1.6.1 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md#161---2024-05-21-estimated)


## 1.6.1 

Tapis 1.6.1 contains a number of new features, enhancements and bug fixes.  In addition to across-the-board dependency updates, significant new capabilities are highlighted below. More detail can be found in the Changelog for each of the services.

### Service Updates

- [Security: 1.6.0 to 1.6.1 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
  - Improved performance of role and permission APIs.
- [Systems: 1.6.0 to 1.6.1 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
  - Upgraded DTN support (breaking change for existing DTN users only)
  - Added system ID parameter on initial Globus authentication (breaking change).
  - Extended tenant administrator's ability to list systems.
- [Apps: 1.6.0 to 1.6.1 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/dev/CHANGELOG.md)
  - Upgraded DTN support (breaking change for existing DTN users only)
  - Allow enable/disable of specific application versions.
  - Added envKey attribute for file inputs.
- [Jobs: 1.6.0 to 1.6.1 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
  - Upgraded DTN support (breaking change for existing DTN users only)
  - Added envKey attribute for file inputs.
  - Added job termination condition code.
- [Files: 1.6.0 to 1.6.1 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
  - Regex/glob matching for file listings on POSIX systems.
  - Refactored codebase to improve reliability.
- [Notifications: 1.6.0 to 1.6.1 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
- [Globus-Proxy: 1.6.0 to 1.6.1 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)



## 1.6.0 

### Service Updates

- [Abaco: 1.5.0 to 1.6.0 (abaco/core-v3)](https://github.com/TACC/abaco/blob/prod-v3/CHANGELOG.md)
- [Apps: 1.5.10 to 1.6.0 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/dev/CHANGELOG.md)
- [Authenticator: 1.5.1 -> 1.6.0 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/dev/CHANGELOG.md)
- [Files: 1.5.10 to 1.6.0 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Globus-Proxy: 1.5.0 to 1.6.0 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)
- [Jobs: 1.5.10 to 1.6.0 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Meta: 1.5.10 to 1.6.0 (tapis/metaapi, tapis-meta-rh-server)](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
- [Notifications: 1.5.12 to 1.6.0 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
- [Security: 1.5.10 to 1.6.0 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Systems: 1.5.10 to 1.6.0 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
- Removed the stern component from monitoring


## 1.5.3

### Services Updates

- [Streams: 1.5.0 -> 1.5.1 (tapis/streams-api)](https://github.com/tapis-project/streams-api/blob/prod/CHANGELOG.md)
- This release also fixes a bug with Streams InfluxDB data location inside the container that was causing saved data to be lost between container restarts.
- [Pods: 1.5.0 to 1.5.3 (tapis/pods-api)](https://github.com/tapis-project/pods_service/blob/prod/CHANGELOG.md)


## 1.5.2

### Services Updates

- [Systems: 1.5.0 to 1.5.10 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/dev/CHANGELOG.md)
- [Apps: 1.5.0 to 1.5.10 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/dev/CHANGELOG.md)
- [Notifications: 1.5.0 to 1.5.10 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
- [Files: 1.5.0 to 1.5.10 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.5.0 to 1.5.10 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Security: 1.5.0 to 1.5.10 (tapis/securitymigrate, securityadmin, securityapi, securityexport)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Meta: 1.5.0 to 1.5.10 (tapis/metaapi)](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
- Rebuild java services with latest shared code to fix JWT validation issue.


## 1.5.1

### Services Updates

- This is a bugfix release to address a small bug with Authenticator in 1.5.0. It is not an critical bug and does not affect Tapis < 1.5.0. 
- [ Authenticator: 1.5.0 -> 1.5.1 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)
- Several bugfixes & improvements to the Docker flavor of deployer.

## 1.5.0 

### Services Updated

- [ Authenticator: 1.4.0 -> 1.5.0 (tapis/authenticator, tapis/authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/dev/CHANGELOG.md]
- [ Streams: 1.4.0 -> 1.5.0 (tapis/streams-api)](https://github.com/tapis-project/streams-api/blob/prod/CHANGELOG.md)
- Other 1.4.x Tapis containers versions will be updated to 1.5.0

## 1.4.3

### Services Updated 

- This release contains several bugfixes & improvements for the Docker flavor of Tapis Deployer. 
- [ Systems: 1.4.1 to 1.4.2 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.4.2/CHANGELOG.md)
- [ Apps: 1.4.1 to 1.4.2 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.4.2/CHANGELOG.md)
- [ Notifications: 1.4.0 to 1.4.1 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/1.4.1/CHANGELOG.md)
- [ Files: 1.4.2 to 1.5.0 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [ Jobs: 1.4.2 to 1.5.0 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [ Globus-Proxy: 1.4.2 to 1.4.3 (tapis/globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)



### Breaking Changes for Deployer Admins

- This is ONLY for Docker Tapis installs updating; it is NOT applicable to Kubernetes installs: Some components' Postgres directory volume mounts have moved within the `tapisdatadir` and may need to be moved on disk before starting the containers. Each component should now follow a similar structure, e.g. for authenticator: `tapisdatadir/authenticator/postgres/data` should contain the Postgres data, such as the `PG_VERSION` file, `pg_wal` directory, etc. 


## 1.4.2

### Services Updated

- [Files: 1.4.1 to 1.4.2 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.4.1 to 1.4.2 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)

## 1.4.1

### Services Updated

- [Systems: 1.4.0 to 1.4.1 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.4.1/CHANGELOG.md)
- [Apps: 1.4.0 to 1.4.1 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.4.1/CHANGELOG.md)
- [Files: 1.4.0 to 1.4.1 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.4.0 to 1.4.1 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)

## 1.4.0

### Services Updated

- All Tapis components will be updated from versions 1.3.x to 1.4.0.
  - [Workflows](https://github.com/tapis-project/tapis-workflows/blob/release-1.4.0/CHANGELOG.md)
  - [Pods](https://github.com/tapis-project/pods_service/blob/prod/CHANGELOG.md#140---2023-07-06)
  - [Systems](https://github.com/tapis-project/tapis-systems/blob/1.4.0/CHANGELOG.md) 
  - [Apps](https://github.com/tapis-project/tapis-apps/blob/local/CHANGELOG.md)
  - [Files](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
  - [Jobs](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
  - [Authenticator](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)
  - [Meta](https://github.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md)
  - [Tenants](https://github.com/tapis-project/tenants-api/blob/dev/CHANGELOG.md)
  - [Tokens](https://github.com/tapis-project/tokens-api/blob/dev/CHANGELOG.md)
  - [Notifications](https://github.com/tapis-project/tapis-notifications/blob/dev/CHANGELOG.md)
  - [Globus-Proxy](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)
  - [Security](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- Nginx locations for individual components have been split into their own location files. Should not cause a breaking change or interrupt routing. 

### Breaking Changes for Services / Tapis Users

- For Systems and Apps: Environment variables beginning with _tapis are no longer valid in the envVariables attribute. (This matches existing Jobs service behavior.) If you are a Tapis user who creates or maintains Systems or Apps resources, creating a resource that specifies an environment variable starting with _tapis will now result in the resource creation to be rejected. If such a resource already exists, future jobs that use it will fail.
- Authenticator:
  - The DELETE /v3/oauth2/clients endpoint now returns the standard 5-stanza Tapis response. Previously, it returned an empty HTTP response. Applications that use this endpoint should be updated to handle a non-empty response.
  - The POST /v3/oauth2/tokens endpoint has been changed in the case of the device_code grant to require only the client_id as a POST parameter. Previously, the client_id and client_key were erroneously both required to be passed using an HTTP Basic Auth header. Client applications that utilized the device code grant type and passed the client credentials as part of the HTTP Basic Auth header must be updated to pass only the client id as part of the POST payload. The OA3 spec has been updated to reflect this new requirement. See issue #32.
- Globus-Proxy:
  - In order for a primary or associate site to support Tapis systems of type GLOBUS, a Globus project must be created and registered. This yields a Globus client ID that must be configured as part of the Tapis environment. For more information please see:
https://tapis.readthedocs.io/en/latest/deployment/deployer.html#configuring-support-for-globus (This is not a breaking change per se, but is required for Globus-Proxy to function.)

### Deployer Updates

- Nginx locations for individual components have been split into their own location files. This should not cause a breaking change or interrupt routing.

### Breaking Changes for Deployer Admins

- None

## 1.3.8

- Added java heap max and min options for apps, systems, and notifications when using Docker compose.
- [Jobs: 1.3.4 to 1.3.5 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Systems: 1.3.2 to 1.3.3 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.3.3/CHANGELOG.md)
- [Files: 1.3.5 to 1.3.6 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Pods: 1.3.0 to 1.3.1 (tapis/pods-api)](https://github.com/tapis-project/pods_service/blob/prod/CHANGELOG.md#131---2023-06-06)
- [Abaco: 1.3.0 to 1.3.1 (abaco/core-v3)](https://github.com/TACC/abaco/blob/prod-v3/CHANGELOG.md#131---2023-06-06)
- Refactored deployment scripts for files and added a script to create the files db if it doesn't exist
- Docker Flavor update:  
  - Added verification scripts for more core components
  - Changed secrets to using a python script for parsing instead of bash scripting 
  - Added a DB init script for files
  - Removed hard-coded urls in proxy
  - General cleanup & bugfixes

### Breaking Changes

- There is a breaking change related to how Files and Systems interact for systems of type IRODS. Please see the [CHANGELOG](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md) for the Files service for more information.

## 1.3.7

- [Authenticator: 1.3.3 to 1.3.4 (authenticator & authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/prod/CHANGELOG.md)
- [Notifications: 1.3.3 to 1.3.4 (notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/1.3.4/CHANGELOG.md)
- [Globus Proxy: 1.3.0 to 1.3.1 (globus-proxy)](https://github.com/tapis-project/globus-proxy/blob/dev/CHANGELOG.md)
- Added optional `skadmin_sk_privileged_sa` var to skadmin component to enable Kubernetes privilege separation.
- Beta release: A new way of deploying Tapis using Docker instead of Kubernetes is now in Beta. By setting `tapisflavor: docker` in the Ansible config, Deployer uses a different set of templates to create the Docker-based Tapis installation scripts. So far only a subset of the components are functional. 

## 1.3.6

- [Authenticator: 1.3.0 to 1.3.3 (authenticator & authenticator-migrations)](https://github.com/tapis-project/authenticator/blob/prod/CHANGELOG.md)
- [Jobs: 1.3.2 to 1.3.4 (tapis/jobsapi, tapis/jobsmigrate, tapis/jobsworker)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [SK 1.3.1 to 1.3.2 (tapis/securitymigrate, tapis/securityexport, tapis/securityadmin, tapis/securityapi)](https://github.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md)
- [Systems: 1.3.1 to 1.3.2 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.3.2/CHANGELOG.md)
- [Apps: 1.3.2 to 1.3.3 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.3.3/CHANGELOG.md)
- [Notifications: 1.3.1 to 1.3.3 (tapis/notifications, notifications-dispatcher)](https://github.com/tapis-project/tapis-notifications/blob/1.3.3/CHANGELOG.md)


## 1.3.5

**Breaking Changes**

Previous versions of Tapis Deployer have placed important vault configs in ~/vault, ~/vault-token. These files are now moved to a configurable directory set by the `tapisdatadir` variable. This should be set to the directory on your deployment machine that contains data for your installation and should

**If you migrating from an existing Tapis deployement** be sure to copy:
- create the `tapisdatadir`/vault directory
- copy ~/vault file to `tapisdatadir`/vault/vault-init file
- copy ~/vault-token file to `tapisdatadir`/vault/vault-token file


Other changes:

Image updates for:

- Systems: 1.3.0 to 1.3.1 (tapis/systems)
- Apps: 1.3.1 to 1.3.2 (tapis/apps)
- Notifications: 1.3.0 to 1.3.1 (tapis/notifications,notifications-dispatcher)
- Jobs: 1.3.1 to 1.3.2 (tapis/jobsworker, jobsmigrate, jobsapi)
- SK: 1.3.0 to 1.3.1 (tapis/securitymigrate, securityexport, securityadmin, securityapi)
- Files: 1.3.2 to 1.3.3 (tapis/tapis-files and tapis/tapis-files-workers)


## 1.3.4

- Vault config (vault.hcl) fixes

## 1.3.3

- Updated security images to 1.3.1 

## 1.3.2

- Updated several image minor release versions. 
- Added VERSION file to reflect which version of tapis-deployer was used.

**Breaking Changes**

- If you have an existing Tapis deployment, you may be using the "file" storage type for vault. In the future the default will use "raft" storage type. For new installs, no action is required. Follow Migration steps below to migrate from file to raft storage.

### Migration from 1.2.x steps 

- Check your existing vault for storage type. Exec into the container and get storage type

    kubectl exec -it deploy/vault vault status | grep "Storage Type"
    Storage Type    file

If your storage type if "file", include this in your host_vars:

    vault_raft_storage: false

If your storage type is "raft", no further action required. Ensure that "vault_raft_storage" var is undefined in your host_vars.

## 1.3.0 

**Breaking Changes**

- Tapis Deployer 1.3.0 differs greatly from 1.2.x. Please refer to the documentation https://tapis.readthedocs.io/en/latest/technical/index.html for migration guide.  
- The template generation backend was redone using Ansible.
- The input generator is deprecated.

### Migration from 1.2.x steps 

- Remove "tokens_tenants" var from the tokens section of your input file. Is now set to ["*"] by default, meaning tokens will get a list of tenants from tenants service.
- Remove "authenticator_service_tenants" var from the authenticator section of your input file. Is now set to ["*"] by default, meaning authenticator will get a list of tenants from tenants service.
- Update your host_vars (deployer input file) to include the following new variables. (see inventory_examples for reference):

    # Choose where your deployment files should be created.
    tapisdir: '{{ ansible_env.HOME }}/tmp/{{ inventory_hostname }}'
    tapisdatadir: '{{ ansible_env.HOME }}/tmp/{{ inventory_hostname }}-data'


## 1.2.x - 2023-01-06 

- Docker flavor: Proxy/Nginx: Moved each location stanza to its own file.


## 1.2.0 - 2022-05-31

This is the initial release of Tapis Deployer components.

It attempts to reconcile differences between input files and generator checks.

### Breaking Changes:
- None.

### New features:
- Created input generator.
- Add more checks to ensure the vault is running before starting other services.
- Add workflows service.
- Add container-registry service.
- Add globus-proxy service.


### Bug fixes:
- None.


## 0.9.1 - 2022-01-13

-

## 0.9.0 - 2022-01-12

Initial pre-release of Tapis Deployer for generating Tapis deployment YAML & scripts.

### Breaking Changes:

- Initial release.

### New features:

 - Initial release.

### Bug fixes:

- None.
