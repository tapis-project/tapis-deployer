# Changelog 

Notable changes between versions.

## 1.3.2

- Updated several image minor release versions. 
- Added VERSION file to relfect which version of tapis-deployer was used.

## 1.3.0 - 20230131

### Breaking Changes:


### Migration from 1.2.0 steps 

- Remove "tokens_tenants" var from the tokens section of your input file. Is now set to ["*"] by default, meaning tokens will get a list of tenants from tenants service.
- Remove "authenticator_service_tenants" var from the authenticator section of your input file. Is now set to ["*"] by default, meaning authenticator will get a list of tenants from tenants service.
- Update your host_vars (deployer input file) to include the following new variables. (see inventory_examples for reference):

    global_tapis_domain: <your_domain>
    global_service_url: https://admin.'{{ global_tapis_domain }}'
    global_primary_site_admin_tenant_base_url: '{{ global_service_url }}'
    global_devtenant_url: https://dev.'{{ global_tapis_domain }}'


 

# Choose where your deployment files should be created.
tapisdir: '{{ ansible_env.HOME }}/tmp/{{ inventory_hostname }}'
tapisdatadir: '{{ ansible_env.HOME }}/tmp/{{ inventory_hostname }}-data'

      
### tapis vars
global_tapis_domain: quick.example.com
global_service_url: https://admin.'{{ global_tapis_domain }}'
global_primary_site_admin_tenant_base_url: '{{ global_service_url }}'
global_devtenant_url: https://dev.'{{ global_tapis_domain }}'
global_site_id: tapis
global_storage_class: default
global_vault_url: http://vault:8200




### Bug fixes:

### Other:

- Cleaned up some outdated documentation.

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
