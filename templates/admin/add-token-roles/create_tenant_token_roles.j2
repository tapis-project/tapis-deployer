'''
1. create roles: 
  tenant_creator -- tenant creator role. (needs to be owned/checked by tenants service)
  dev_token_generator -- create tokens in dev role (needs to be owned/checked by tokens api).
  tacc_token_generator -- create tokens in tacc role (needs to be owned/checked by tokens api).

2. put some service in the tenants_creator role
3. put authenticator in the dev_token_generator and tacc_token_generator roles.
3. create the tacc tenant.
'''

import os
from tapy.dyna import DynaTapy


password = os.environ.get('tenants_service_password')
if not password:
    print("Did not fing tenants_service_password variable, exiting...")
    raise Exception()

url = os.environ.get('service_tenant_base_url', 'https://admin.develop.tapis.io')
print(f"targetting {url}")

t = DynaTapy(base_url='https://admin.develop.tapis.io', username='tenants', account_type='service', service_password=os.environ.get('tenants_service_password'))
t.get_tokens()
print("client created..")

# tenant_create role ----
t.sk.createRole(tenant='admin', user='tenants', roleName='tenant_creator', description='Role for creating tenants.')
t.sk.grantRole(tenant='admin', user='tenants', roleName='tenant_creator')
print("tenant_creator role created and granted")

t.sk.createRole(tenant='admin', user='tokens', roleName='dev_token_generator', description='Role for creating tokens in the dev tenant.')
t.sk.createRole(tenant='admin', user='tokens', roleName='tacc_token_generator', description='Role for creating tokens in the tacc tenant.')
t.sk.grantRole(tenant='admin', user='authenticator', roleName='dev_token_generator')
t.sk.grantRole(tenant='admin', user='authenticator', roleName='tacc_token_generator')
print("token roles created.")

