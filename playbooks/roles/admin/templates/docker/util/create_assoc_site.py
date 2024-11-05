import os
import sys 
import json
import argparse
import requests

## import local libs
sys.path.append(os.path.abspath('../base'))
from get_client import get_client

# Description:
## This script will create a new associate site based on a provided json record

# Usage:
## This script will create an associate site record at a primary site, create its admin and dev tenants, and update the pubkeys for those tenants.
## You will need to first have:
## 1. a primary site (or identify the one you want to add an associate site to) and create an entry for it in the ../base/conf.json file, including its base_url e.g. https://admin.develop.tapis.io and a JWT that authenticates as the tenants sercvice for that site. The path to this file will be given with the '-e' flag when running the script
## 2. a complete associate site record .json file, including site data and owner data. An Example of the requisite format is provided at ./test.json. The path to this file will be given with the '-d' flag when running the script. 
### Note that until you do the initial deployment of the associate site, you will not have access to the pubkeys that need to be included in the site record's json file. You will need to run through the steps to create the associate site record, do the initial deployment of the associate site to get the pubkeys, update the site record with those keys, then run this script again.

# Script Steps:
## 1. Create the associate site record, and create the associate site's admin and dev tenant records in "draft" mode.
## 2. Run the initial service deployment at the associate site to generate a public/private key pair for the admin and dev tenants.
## 3. Insert the public key into the tenant record and update the admin and dev tenants to "active".
## 4. Deploy the rest of the services on the associate site.

## global vars
CONF_PATH = os.path.abspath('../base/conf.json')

## get the config per enviroment
def get_conf(env):
    config = ''
    with open(CONF_PATH) as f:
        config = json.load(f)
    return config[env]

def get_jwt_signing_keys(envpath):
    admin_tenant_public_key = ''
    dev_tenant_public_key = ''
    with open(envpath) as f:
        file = f.read()
        admin_index = file.find('admin_tenant_public_key=')
        after = file[admin_index:].split('admin_tenant_public_key="')[1]
        admin_tenant_public_key = after.split('"')[0]

        dev_index = file.find('dev_tenant_public_key=')
        after = file[dev_index:].split('dev_tenant_public_key="')[1]
        dev_tenant_public_key = after.split('"')[0]
        return admin_tenant_public_key, dev_tenant_public_key
    
def update_config(filepath, config: dict):
    '''
    Performs an update-in-place of the provided site config data file with the dict in the 'config' arg. e.g. {thing: thing, thing2, thing2}, {thing: thing2} -> {thing: thing2, thing2: thing2}
    '''
    config = json.loads(json.dumps(config))
    new_config = {}
    with open(filepath, 'r') as f:
        old_config = json.load(f)
        site_data = old_config['site']
        old_config['site']['admin_public_key'] = ""
        old_config['site']['dev_public_key'] = ""

        # print(json.dumps(old_config).replace('\'', '"'))

        for key in set(site_data.keys()).intersection(config.keys()):
            site_data[key] = config[key]
        old_config['site'] = site_data
        # print((json.dumps(old_config).replace('\'', '"')))
        new_config = json.dumps(old_config, indent=4).replace('\'', '"')
        f.close()
    f = open(filepath, 'w')
    f.write(new_config)
    f.close()

def parse_site_data(path):
    data = json.load(open(path))
    site = data['site']
    owner = data['owner']

    
    if set([",", "-", "."]).intersection(set([char for char in site['site_id']])):
        print("ERROR -- assoc_site_id can only contain alpha-numeric string.")
        raise

    if set([",", "-", "."]).intersection(set([char for char in site['site_admin_tenant_id']])):
        print("ERROR -- assoc_site_admin_tenant_id can only contain alpha-numeric string.")
        raise

    for k, v in site.items():
        if type(v) == str and 'todo' in v:
            print(f"ERROR -- {k} is required.")
            break
    else:
        print("site description validated.")

    return site, owner

def get_base_url(tenant, site):
    return f'https://{tenant}.{site}'

## get an authenticated Tapis client using the tenants JWT provided in ../base/conf.json
def get_tapis(tenant, site, jwt):
    print(f'attempting to get authenticated tapis client ...')
    t = get_client(tenant=tenant, site=site, service_jwt=jwt, u='tenants')
    print(f'success! {t}')

    print(f'attempting to check access to tenant "{tenant}" ...')
    
    # check access
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    t.tenants.get_tenant(tenant_id='admin', headers=headers)
    return t

## utility functions
def owner_exists(owner):
    email = owner['email']
    url = f'{primary_site_base_url}/v3/tenants/owners/{email}'
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    rsp = requests.get(url, headers=headers)
    try:
        rsp.raise_for_status()
        # print("200 response.")
        # print(rsp.json())
    except:
        if rsp.status_code == 400:
            # print('owner not found')
            return False
        else:
            print(f'Unexpected result checking if owner exists:: {rsp.json()}')
    return True

def create_owner(owner):
    url = f'{primary_site_base_url}/v3/tenants/owners'
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    rsp = requests.post(url, headers=headers, json=owner)
    # rsp = requests.get(url, headers=headers)
    try:
        rsp.raise_for_status()
        print("200 response.")
        print(rsp.json())
    except:
        print("Request resulted in a non-200 code. See response below:")
        print(rsp.json())

def site_exists(site):
    site_id = site['site_id']
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    url = f'{primary_site_base_url}/v3/sites/{site_id}'
    rsp = requests.get(url, headers=headers)
    try:
        rsp.raise_for_status()
        # print("200 response.")
        # print(rsp.json())
    except:
        if rsp.status_code == 400:
            # print('owner not found')
            return False
        else:
            print(f'Unexpected result checking if owner exists:: {rsp.json()}')
    return True

def create_assoc_site(primary_site_base_url, site, jwt, tid):
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': tid, 
        'X-Tapis-User': 'tenants'
    }
    url = f'{primary_site_base_url}/v3/sites'
    rsp = requests.post(url, headers=headers, json=site)
    try:
        rsp.raise_for_status()
        print("200 response.")
        print(rsp.json())
    except:
        print("Request resulted in a non-200 code. See response below:")
        print(rsp.json())

def tenant_exists(tenant):
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    url = f'{primary_site_base_url}/v3/tenants/{tenant}'
    rsp = requests.get(url, headers=headers)
    try:
        rsp.raise_for_status()
    except:
        if rsp.status_code == 400:
            return False
        else:
            print(f'Unexpected result checking if owner exists:: {rsp.json()}')
    return True

def create_tenant(site, owner, jwt, tenant_type):
    '''
    params:
    - site: assoc site record from {site}.json
    - owner: owner record from {site}.json
    - jwt: primary site tenants service jwt from conf.json
    - tenant_type: either 'dev' or 'admin', matches site_{tenant_type}_tenant_id in {site}.json
    '''
    tenant_id = site[f'site_{tenant_type}_tenant_id']
    site_id = site['site_id']
    assoc_tenant_id = site[f'site_{tenant_type}_tenant_id']
    # assoc_base_url = site['base_url']
    assoc_base_url = get_base_url(tenant_id, site['base_url'])
    assoc_site_owner = owner['email']
    assoc_site_description = f'{tenant_type} tenant for the {site_id} site.'
    assoc_site_admin_user = 'admin'
    assoc_site_token_gen_services = ["authenticator"]

    assoc_admin_tenant = {
        "tenant_id": assoc_tenant_id,
        "base_url": assoc_base_url,
        "token_service": f"{assoc_base_url}/v3/tokens",
        "security_kernel": f"{assoc_base_url}/v3/security",
        "owner": assoc_site_owner,
        "description": assoc_site_description,
        "authenticator": f"{assoc_base_url}/v3/oauth2",
        "site_id": site['site_id'],
        "admin_user": assoc_site_admin_user,
        "token_gen_services": assoc_site_token_gen_services,
        "status": "draft"    
    }
    url = f'{primary_site_base_url}/v3/tenants'
    headers = {
        'X-Tapis-Token': jwt, 
        'X-Tapis-Tenant': 'admin', 
        'X-Tapis-User': 'tenants'
    }
    # print(headers)
    rsp = requests.post(url, headers=headers, json=assoc_admin_tenant)
    try:
        rsp.raise_for_status()
        print("200 response.")
        print(rsp.json())
    except:
        print("Request resulted in a non-200 code. See response below:")
        print(rsp.json())


def update_pubkey(site, tenant):
    key = site[f'{tenant}_public_key']
    # print(f'got key:: {key}')
    tenant_id = site[f'site_{tenant}_tenant_id']
    url = f'{primary_site_base_url}/v3/tenants/{tenant_id}'
    headers = {'X-Tapis-Token': jwt, 'X-Tapis-Tenant': 'admin', 'X-Tapis-User': 'tenants'}
    data = {'status': 'active', 'public_key': key}
    if not key:
        print('error -- you must fill in the public key')
    else:
        rsp = requests.put(url, headers=headers, json=data)
        print(rsp.json())


## main script
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--primary-site', '-p', dest='env', default='develop', help='The enviroment that we wish to add an assoc site to. These are defined in ../base/conf.json')
    p.add_argument('--def', '-d', dest='site_record', required=True, help='The path to the file containing a json representation of the site data')
    args = p.parse_args()

    print('\n\n### Parse Args ###')
    config = json.loads(json.dumps(get_conf(args.env)))
    print(f'Loaded config from {args.env}: {config}')

    primary_site_base_url = config['base_url']
    jwt = config['jwt']
    print(f'have jwt:: {jwt}')

    url_args = primary_site_base_url.replace('https://', '').split('.', 1)

    tenant = url_args[0]
    site = url_args[1]

    print('\n\n### Get Service Client ###')
    print(f'attempting to get a tapis with... \n\ttenant={tenant}\n\tsite={site}\n\tjwt={jwt}\n\t')
    t = get_tapis(tenant, site, jwt)

    print('\n\n### Parse Site Data ###')
    ## parse site data from given file
    site, owner = parse_site_data(args.site_record)

    ## create the owner if it doesn't exist
    print(f'\n\n### Owner ### ')
    name = owner['name']
    email = owner['email']
    if not owner_exists(owner):
        print(f'owner "{name}" with email {email} not found. Creating ...')
        create_owner(owner)
    else:
        print(f'Owner "{name}" with email {email} already exists. Skipping creation ')

    ## create the site if it doesn't exist
    print(f'\n\n### Site ###')
    site_id = site['site_id']
    if not site_exists(site):
        print(f'site "{site_id}" does not exist. Creating ... ')
        create_assoc_site(primary_site_base_url, site, jwt, tenant)
    else:
        print(f'Site "{site_id}" already exists. Skipping creation ')
    
    ## create the admin tenant if it doesn't exist
    print(f'\n\n### Admin Tenant ###')
    tenant_id = site['site_admin_tenant_id']
    site_id = site['site_id']
    if not tenant_exists(site['site_admin_tenant_id']):
        print(f'Tenant "{tenant_id}" does not exist at site "{site_id}". Creating ...')
        create_tenant(site, owner, jwt, 'admin') 
    else:
        print(f'Tenant "{tenant_id}" already exists at site "{site_id}". Skipping creation')

    ## create the dev tenant if it doesn't exist
    print(f'\n\n### Dev Tenant ###')
    tenant_id = site['site_dev_tenant_id']
    site_id = site['site_id']
    if not tenant_exists(site['site_dev_tenant_id']):
        print(f'Tenant "{tenant_id}" does not exist at site "{site_id}". Creating ...')
        create_tenant(site, owner, jwt, 'dev')
    else:
        print(f'Tenant {tenant_id} already exists at site {site_id}. Skipping creation')

    ## Update pubkey for admin and dev tenants
    print(f'\n\n### Update Pubkeys ###')
    # admin_pubkey = site['admin_public_key']
    # dev_pubkey = site['dev_public_key']
    admin_pubkey = site.get('admin_public_key')
    dev_pubkey = site.get('dev_public_key')
    if not admin_pubkey or not dev_pubkey:
        print(f'Pubkeys are not provided in the site record. Assuming that the initial associate site deployment has not bee run. Do the initial deployment, update the site record with the pubkeys, then run this script again.')
        exit(0)

    ### admin
    update_pubkey(site, 'admin')

    ### dev
    update_pubkey(site, 'dev')

    ## will need to restart tenants before the changes can take effect
