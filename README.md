# Tapis-Deployer
Repo for code for tapis-deployer
---
## ymlGenerator use
Generates a yaml file from an input yaml file based on the ymlTemplate.txt in the templates folder if the output file is specificed. 
If there is not specified output file the program will just take the input yaml file and print it out in the ~/tmp/taps-deploy/tenants.

[Link to google drive](https://drive.google.com/drive/folders/1lDgt-i3khEwJjzINGzK4FjX9x5NNlmT8?usp=sharing)


Program with no arguments
```
python3 ymlGenerator.py
usage: ymlGenerator.py [-h] [-o [outFile]] [inFile]

Generate yaml config file

positional arguments:
  inFile        File location of yaml config

optional arguments:
  -h, --help    show this help message and exit
  -o [outFile]  File location of output file
```
Program with output file 
```
python3 ymlGenerator.py -o Test/output.yml Test/input.yml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  textmode: True
  service_tenant_base_url: https://admin.develop.tapis.io
  sql_db_url: postgres://tenants:blahpassword1@tenants-postgres:5432/tenants
spec:
  textmode: True
  service_tenant_base_url: https://admin.develop.tapis.io
  sql_db_url: postgres://tenants:blahpassword1@tenants-postgres:5432/tenants
```
Program with no output file
```
python3 ymlGenerator.py templates/tenants-api/api-deploy.yml 
{'kind': 'Deployment', 'spec': {'template': {'spec': {'containers': [{'ports': [{'name': 'http', 'containerPort': 5000}], 'image': 'tapis/tenants-api:dev', 'volumeMounts': [{'mountPath': '/home/tapis/config.json', 'subPath': 'config.json', 'name': 'tenants-config'}], 'name': 'tenants-api', 'imagePullPolicy': 'Always'}], 'volumes': [{'configMap': {'name': 'tenants-config'}, 'name': 'tenants-config'}]}, 'metadata': {'labels': {'app': 'tenants-api'}}}, 'selector': {'matchLabels': {'app': 'tenants-api'}}}, 'apiVersion': 'apps/v1', 'metadata': {'name': 'tenants-api'}}

```
