import argparse
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
import os

parser = argparse.ArgumentParser(description="Generate yaml config file")
parser.add_argument('input', metavar='inFile', nargs='?',type=argparse.FileType('r'), 
                    help="File location of yaml config")

file_loader = FileSystemLoader('TACCSummerInternship2021/templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit()

parameters = yaml.load(args.input)

for foldername, files in parameters["tenants-api"].items():
    for NULL, file in  files.items():
        template = env.get_template("tenants-api/" + file["template"])
        # try:
        #     file_path = os.path.expanduser('~/tmp/tapis-deploy/tenants-api' + "/" + foldername) + "/" + file["name"]
        #     with open(file_path, "w") as f:
        #         # doc = yaml.dump(parameters, file)
        #         f.write(template.render())
        # except:
        #     os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/tenants-api' + "/" + foldername)) 
        #     file_path = os.path.expanduser('~/tmp/tapis-deploy/tenants-api' + "/" + foldername) + "/" + file["name"]
        #     with open(file_path, "w") as f:
        #         # doc = yaml.dump(parameters, file)
        #         f.write(template.render())
        try:
            os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/tenants-api' + "/" + foldername)) 
        except:
            pass
        file_path = os.path.expanduser('~/tmp/tapis-deploy/tenants-api' + "/" + foldername) + "/" + file["name"]
        with open(file_path, "w") as f:
            # doc = yaml.dump(parameters, file)
            f.write(template.render())