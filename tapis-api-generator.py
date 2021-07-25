import argparse
import yaml
from jinja2 import Environment, FileSystemLoader
import os
from shutil import copyfile

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

def write_tapis(input_yaml, path, uni_param="", ser_param=""):
    for obj, data in input_yaml.items():
        if obj == "universal-parameters":
            uni_param = data 
        elif obj == "service-parameters":
            ser_param = data
        elif "file_ext" in data:
            file_path = path + obj + data["file_ext"]
            if data["template"].split(".")[-1] == "j2":
                template = env.get_template(path + data["template"])
                with open(os.path.expanduser("~/tmp/tapis-deploy/") + file_path, "w") as file:
                    try:
                        file.write(template.render(local_param=data['data'], service_param=ser_param['data'],universal_param=uni_param['data']))
                    except:
                        file.write(template.render())         
        else:
            write_tapis(data, path + obj + "/", uni_param, ser_param)   
    return

def create_tapis(template_path):
    for root, dir, files in os.walk(template_path):
        root = root[root.index("/")+1:] + "/"
        for name in dir:
            try:
                os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/' + root + name))
            except:
                pass
        for name in files:
            if name.split(".")[-1] != "j2":
                copyfile(template_path + root + name, os.path.expanduser("~/tmp/tapis-deploy/") + root + name)


def main():
    parser = argparse.ArgumentParser(description="Generate yaml config file")
    parser.add_argument('input', metavar='inFile', nargs='?',type=argparse.FileType('r'), 
                        help="File location of yaml config")

    args = parser.parse_args()
    if not args.input:
        parser.print_help()
        exit()

    parameters = yaml.load(args.input)

    try:
        os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/'))
    except:
        pass

    file_path = ""

    create_tapis(template_path= "templates/")
    write_tapis(parameters, file_path)

if __name__ == '__main__':
    main()