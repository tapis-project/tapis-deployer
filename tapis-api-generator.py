import argparse
import yaml
from jinja2 import Environment, FileSystemLoader
import os
from shutil import copy

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

def write_tapis(input_yaml, path, service_list, outDir = os.path.expanduser('~/tmp'), defaults_file="", uni_param="", ser_param={"data": ""}, is_sub=False):
    for obj, data in input_yaml.items():
        if obj == "universal-parameters":
            uni_param = data 
        elif obj == "service-parameters":
            ser_param = data
        elif "file_ext" in data:
            file_path = path + obj + data["file_ext"]
            if data["template"].split(".")[-1] == "j2":
                if "template_directory" in ser_param['data']:
                    new_path = path.split("/")
                    new_path[0] = ser_param['data']["template_directory"]
                    new_path = '/'.join(new_path) 
                    template = env.get_template(new_path + data["template"])
                    permissions = (os.stat("templates/" + new_path + data["template"])[0])
                else:
                    template = env.get_template(path + data["template"])
                    permissions = (os.stat("templates/" + path + data["template"])[0])
                def_param = defaults_file["defaults"]["universal"]
                try:
                    def_param.update(defaults_file["defaults"][ser_param["data"]["service_name"]])
                except:
                    pass
                with open(outDir + "/tapis-deploy/" + file_path, "w") as file:
                    file.write(template.render(local_param=data['data'], service_param=ser_param['data'], universal_param=uni_param['data'], service_list = service_list, defaults=def_param))
                    os.chmod(outDir + "/tapis-deploy/" + file_path, permissions)
        else:
            if(obj not in service_list and not is_sub):
                continue
            try:
                os.makedirs(outDir + "/tapis-deploy/" + path + obj)
            except:
                pass
            write_tapis(data, path + obj + "/", service_list, outDir, defaults_file, uni_param, ser_param, True)   
    return

def create_tapis(template_path, service_list, outDir = os.path.expanduser('~/tmp')):
    for root, _, files in os.walk(template_path, topdown=False):
        service = root.split('/')[1]
        if(service not in service_list and service != ""):
            continue
        root = root[root.index("/")+1:] + "/"
        for name in files:
            try:
                os.makedirs(outDir + '/tapis-deploy/' + root)
            except:
                pass
            if name.split(".")[-1] != "j2":
                copy(template_path + root + name, outDir + "/tapis-deploy/" + root + name)


def main():

    import os 
    basedir = os.path.dirname(os.path.realpath(__file__))
    print(basedir)

    parser = argparse.ArgumentParser(description="Generate yaml config file")
    parser.add_argument('input', metavar='inFile', nargs='?',type=argparse.FileType('r'), 
                        help="File location of yaml config")

    parser.add_argument('-o', dest='outDir', metavar='outDir', nargs='?',
                        help="File location of program output, if not specified defaults to tmp/tapis-deploy")

    args = parser.parse_args()
    if not args.input:
        parser.print_help()
        exit(1)

    parameters = yaml.safe_load(args.input)
    f = open("defaults.yml", "r")
    defaults = yaml.safe_load(f)
    outDir = args.outDir
    service_list = parameters.get("services")
    file_path = ""

    if(outDir):
        outDir = outDir.strip()
        try:
            test = outDir+"/tapis-deploy/"
            test2 = os.path.expanduser(test)
            os.makedirs(test2)
        except:
            pass
        create_tapis("templates/", service_list, os.path.abspath(outDir))
        write_tapis(parameters, file_path, service_list, os.path.abspath(outDir), defaults_file=defaults)
    else:
        try:
            os.makedirs(os.path.expanduser('~/tmp/tapis-deploy/'))
        except:
            pass
        create_tapis("templates/", service_list)
        write_tapis(parameters, file_path, service_list, defaults_file=defaults)

if __name__ == '__main__':
    main()
