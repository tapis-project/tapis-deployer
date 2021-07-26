import argparse
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
import os

parser = argparse.ArgumentParser(description="Generate yaml config file")
parser.add_argument('input', metavar='inFile', nargs='?',type=argparse.FileType('r'), 
                    help="File location of yaml config")

parser.add_argument('-o', dest='outFile', metavar='outFile', nargs='?',type=argparse.FileType('w'), 
                    help="File location of output file")


args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit()

parameters = yaml.load(args.input)
print(parameters['service_tenant_url'])

file_loader = FileSystemLoader('TACCSummerInternship2021/templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

template = env.get_template('global-config.j2')

# print(template.render(parameters=parameters))
if args.outFile:
    args.outFile.write(template.render(service_tenant_url=parameters['service_tenant_url']))
else:
    try:
        file_path = os.path.expanduser('~/tmp') + "/global-config.yml" 
    except:
        os.makedirs(os.path.expanduser('~/tmp'))
        file_path = os.path.expanduser('~/tmp')  + '/global-config.yml'
    with open(file_path, "w") as file:
        # doc = yaml.dump(parameters, file)
        file.write(template.render(service_tenant_url=parameters['service_tenant_url']))