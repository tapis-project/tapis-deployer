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
print(parameters)

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

template = env.get_template('ymlTemplate.txt')

# print(template.render(parameters=parameters))
if args.outFile:
    args.outFile.write(template.render(parameters=parameters))
else:
    try:
        file_path = os.path.expanduser('~/tmp/tapis-deploy/tentants/') + args.input.name.split("/")[-1]
        with open(file_path, "w") as file:
            doc = yaml.dump(parameters, file)
    except:
        os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/tentants-api/'))
        file_path = os.path.expanduser('~/tmp/tapis-deploy/tentants-api/') + args.input.name.split("/")[-1]
        with open(file_path, "w") as file:
            doc = yaml.dump(parameters, file)