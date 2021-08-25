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
