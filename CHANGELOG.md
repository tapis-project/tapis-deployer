# Changelog 

Notable changes between versions.

## 1.3.5

Image updates

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

## 1.3.0 

**Breaking Changes**

- Tapis Deployer 1.3.0 differs greatly from 1.2.x. Please refer to the documentation https://tapis.readthedocs.io/en/latest/technical/index.html for migration guide.  
- The template generation backend was redone using Ansible.
- The input generator is deprecated.



## 1.3.0 - 20230106 

### Breaking Changes:


### New features:

- Proxy/Nginx: Moved each location stanza to its own file.


### Bug fixes:




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
[tapistest@cic02 tapis-deployer]$
