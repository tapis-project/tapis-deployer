# Tapis Deployer 

This tool generates the scripts and Kubernetes YAML used to stand up an instance of Tapis.

## Usage

tapis-api-generator.py generates all the scripts and YAML from templates. You must first provide an input YAML that describes the specifics of your site.


## Run input-generator

This script helps to build up your input YAML.

TBD


## Run tapis-api-generator.py


Once you have your input YAML you can generate your Tapis deployment. 


Script help:

    python3 ~/tapis-deployer/tapis-api-generator.py --help

Example of how to run:

    python3 ~/tapis-deployer/tapis-api-generator.py --destdir ~/tmp/tapis-kube --input ~/tmp/test-primary.tapis.io.yml 

# Tapis Site Types

There are two types of Tapis site, with different config options for each.


## Creating primany site


## Creating associate site

steps for creating and deploying a new associate site:
1. (pre-req step to running deployer, done by emailing primary site) register the associate site with the sites API
2. (pre-req step to running deployer, done by emailing primary site) register the associate site admin tenant with the primary site tenants API. note: at this step, the tenant will be in DRAFT mode (i.e., not ACTIVE) and will not have a public/private key pair associated with it.
3. deployer at associate site:
a. generate sk-admin JSON files -- specifically, need to generate the tapis-tokens-secrets.json from a template to generate the signing key pair (but will also want to only generate the JSON files for the services being deployed, likely also from templates) 
b. deploy and initialize vault for tapis
4. deployer at associate site: update admin tenant to ACTIVE with public/private key pair:
a. run SK admin to generate public/private key pair for the associate site admin tenant. after this step the public and private key pair for each tenant will be available as k8s secrets.
i. public key gets printed to the screen (or maybe a file).
b. send an email to the primary site admins with the public key so they can update tenants API (running at primary site) with the public key.
5. deployer at associate site: start up tokens and authenticator at associate site.
a. inject the private key generated at step 4a) as a k8s secret into the tokens pod



