import os
from tapy.dyna import DynaTapy

t = DynaTapy(base_url='{{tokens_service_url}}', username='tenants', account_type='service', service_password=os.environ.get('tenants_service_password'))

# tenant_create role ----
t.sk.createRole(tenant='admin', user='tenants', roleName='tenant_creator', description='Role for creating tenants.')
t.sk.grantRole(tenant='admin', user='tenants', roleName='tenant_creator')


t = DynaTapy(base_url='{{tokens_service_url}}', username='tokens', account_type='service', service_password=os.environ.get('tokens_service_password'))
t.sk.createRole(tenant='admin', user='tokens', roleName='dev_token_generator', description='Role for creating tokens in the dev tenant.')
t.sk.createRole(tenant='admin', user='tokens', roleName='tacc_token_generator', description='Role for creating tokens in the tacc tenant.')
t.sk.grantRole(tenant='admin', user='authenticator', roleName='dev_token_generator')
t.sk.grantRole(tenant='admin', user='authenticator', roleName='tacc_token_generator')
