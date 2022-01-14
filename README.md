# Tapis Deployer 

This tool generates the scripts and Kubernetes YAML used to stand up an instance of Tapis.

## ymlGenerator use
Generates a yaml file from an input yaml file based on the ymlTemplate.txt in the templates folder if the output file is specificed. 
If there is not specified output file the program will just take the input yaml file and print it out in the ~/tmp/taps-deploy/tenants.

[Link to google drive](https://drive.google.com/drive/folders/1lDgt-i3khEwJjzINGzK4FjX9x5NNlmT8?usp=sharing)


Program with no arguments
```
python3 tapis-api-generator.py 
usage: tapis-api-generator.py [-h] [-o [outDir]] [inFile]

Generate yaml config file

positional arguments:
  inFile       File location of yaml config

optional arguments:
  -h, --help   show this help message and exit
  -o [outDir]  File location of program output, if not specified defaults to
               tmp/tapis-deploy
```
Program with input specified
```
python3 tapis-api-generator.py Test/input.yml 
```
Program with input and output specified
```
python3 tapis-api-generator.py Test/input.yml -o ../test/
python3 tapis-api-generator.py Test/input.yml -o ~/
```

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



