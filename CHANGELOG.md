# Changelog 

Notable changes between versions.

## 1.4.0

### Services updated:

- [Pods: 1.3.2 to 1.4.0 (tapis/pods-api)](https://github.com/tapis-project/pods_service/blob/prod/CHANGELOG.md#140---2023-07-06)

### Breaking Changes for Services / Tapis Users 

- None

### Deployer updates:

- None

### Breaking Changes for Tapis Deployer Admins

- None


## 1.3.9

### Services updated:

- [Systems: 1.3.3 to 1.3.4 (tapis/systems)](https://github.com/tapis-project/tapis-systems/blob/1.3.4/CHANGELOG.md) 
- [Apps: 1.3.3 to 1.3.4 (tapis/apps)](https://github.com/tapis-project/tapis-apps/blob/1.3.4/CHANGELOG.md)  
- [Files: 1.3.6 to 1.3.7 (tapis/tapis-files, tapis/tapis-files-workers)](https://github.com/tapis-project/tapis-files/blob/dev/CHANGELOG.md)
- [Jobs: 1.3.5 to 1.3.6 (tapis/jobsworker, jobsmigrate, jobsapi)](https://github.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md)
- [Authenticator: 1.3.4 to 1.3.5 (authenticator_api_image, authenticator_migrations_image)](https://github.com/tapis-project/authenticator/blob/staging/CHANGELOG.md)

### Breaking Changes for Services / Tapis Users 

- For Systems and Apps: Environment variables beginning with *_tapis* are no longer valid in the envVariables attribute. (This matches existing Jobs service behavior.) If you are a Tapis user who creates or maintains Systems or Apps resources, creating a resource that specifies an environment variable starting with *_tapis* will now result in the resource creation to be rejected. If such a resource already exists, future jobs that use it will fail.
- Authenticator: 
  - The DELETE /v3/oauth2/clients endpoint now returns the standard 5-stanza Tapis response. Previously, it returned an empty HTTP response. Applications that use this endpoint should be updated to handle a non-empty response.
  - The POST /v3/oauth2/tokens endpoint has been changed in the case of the device_code grant to require only the client_id as a POST parameter. Previously, the client_id and client_key were erroneously both required to be passed using an HTTP Basic Auth header. Client applications that utilized the device code grant type and passed the client credentials as part of the HTTP Basic Auth header must be updated to pass only the client id as part of the POST payload. The OA3 spec has been updated to reflect this new requirement. See issue #32.


### Deployer updates:

- None

### Breaking Changes for Tapis Deployer Admins

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
