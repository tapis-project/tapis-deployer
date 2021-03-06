import json
import re
import requests
from jinja2 import Environment, FileSystemLoader
import argparse
import os
import sys
import yaml

import sys
sys.path.append('/deploygen/lib')
import deployer

# location of yaml description files
INP_DESCS_DIR = '/inputgen/inputdescs'

# location to deploygen templates
DEPLOYGEN_TEMPLATES_DIR = '/deploygen/templates'


# whether to print verbose output
vb = False


# override the SafeDumper to disable the use of YAML aliases and anchors.
# cf., https://github.com/yaml/pyyaml/issues/103
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PRIMARY_SITE_SERVICES = ["actors", "apps", "authenticator", "files", "jobs", "meta",
"monitoring", "notifications", "pgrest", "pods", "security", "streams", "systems", "tenants", "tokens",
"workflows"]


# --------------
# Diagnostics
# --------------

def check_inputgen_templates():
    all_input_descs = {}
    error_templates = 0
    correct_templates = 0
    for f_name in os.listdir(INP_DESCS_DIR):
        with open(os.path.join(INP_DESCS_DIR, f_name), 'r') as f:
            d = f.read()
            if not d:
                print(f"Error: decription file {f_name} is empty.")
                error_templates += 1
            else:
                try:
                    all_input_descs.update(yaml.safe_load(d))
                    correct_templates += 1
                except Exception as e:
                    error_templates
                    print(f"Error: description file {f_name} could not be loaded as yaml. Additional details: {e}")
    if error_templates == 0:
        if vb: print("All yaml description files loaded to Python objects successfully. Now checking required fields...\n")
    # check for required properties
    errors = 0
    warnings = 0
    for k, v in all_input_descs.items():
        # if a value is provided, nothing else is required
        if 'value' in v.keys():
            continue
        if 'description' not in v.keys():
            errors += 1
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has no value property and is missing description field.")
        elif not v.get('description'):
            errors += 1
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has no value property and has an empty description field.{bcolors.ENDC}")
        elif not type(v['description']) == str:
            warnings += 1
            print(f"{bcolors.WARNING}Warning:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has a description field that is not a string.{bcolors.ENDC}")
        else:
            desc = v['description'].lower()
            if 'todo' in desc:
                print(f"{bcolors.WARNING}Warning:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has a todo in the description. Description: {desc}.{bcolors.ENDC}")
        if 'source_vars' not in v.keys():
            errors += 1
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has no value property and is missing description field.{bcolors.ENDC}")
        if 'example' not in v.keys():
            errors += 1
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has no value property and is missing example field.{bcolors.ENDC}")
        elif not v.get('example'):
            errors += 1
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has no value property and has an empty example field.{bcolors.ENDC}")
        else:
            example = v['example']
            # some examples are of type bool or a complex type such as list..
            if type(example) == str:
                example = example.lower()
            if 'todo' in desc:
                warnings += 1
                print(f"{bcolors.WARNING}Warning:{bcolors.ENDC} field {bcolors.OKCYAN}{k}{bcolors.ENDC} has a todo in the example. Description: {example}{bcolors.ENDC}")
    print("\nInputgen Template Totals:")
    print("=========================")
    print(f"Total templates: {error_templates + correct_templates}")
    print(f"Templates that could not be loaded: {error_templates}")
    print(f"Total variables across all loadable inputgen templates: {len(all_input_descs.keys())}")
    print(f"Errors within loadable templates (see messages above): {errors}")
    print(f"Warnings within loadable templates (see messages above): {warnings}")
    return all_input_descs
        

def get_vars_for_template(t):
    """
    Parse a jinja2 template for all variables references, and return as a python list of variable names as strings.
    """
    if vb: print(f"parsing template: {t}")
    result = []
    error = None
    from jinja2 import Environment, PackageLoader, meta
    env = Environment(loader=FileSystemLoader('/'))
    template_source = env.loader.get_source(env, t)
    try:
        parsed_content = env.parse(template_source)
        result = meta.find_undeclared_variables(parsed_content)
    except Exception as e:
        error = f"{t}; error details: {e}"
    return result, error


def check_deploygen_templates(all_input_descs):
    # list of all absolute paths to directories with templates in them
    template_dirs = []
    # list of all template files
    templates = []
    # templates that got errors when trying to parse them to determine the variables associated with them.
    error_templates = {}
    for dirpath, dirnames, filenames in os.walk(DEPLOYGEN_TEMPLATES_DIR):
        for d in dirnames:
            template_dirs.append(os.path.join(dirpath,d))
    for d in template_dirs:    
        tp_files = [os.path.join(d, f) for f in os.listdir(d) if not os.path.isdir(os.path.join(d, f))]
        templates.extend(tp_files)
    # set of all variables in all template files.
    template_vars = set()
    for t in templates:
        # get all variables from the template t
        vars, error = get_vars_for_template(t)
        if error:
            error_templates[t] = error
        else:
            for v in vars:
                template_vars.add(v)
    #
    vars_missing_from_inputgens = []
    # check for variables defined in templates but not in the inputgen
    for v in template_vars:
        if v not in all_input_descs.keys():
            vars_missing_from_inputgens.append(v)

    print("\nDeployergen Template Totals:")
    print("============================")
    print(f"Total templates: {len(templates)} templates.")
    print(f"Templates that could not be loaded: {len(error_templates.keys())}")
    print(f"Total variables across all loadable templates: {len(template_vars)}")
    
    print("\nTemplates that could not be loaded (details):")
    for _, err in error_templates.items():
        print(err)
    print(f"\nTotal variables in deploygen templates but NOT in inputgen: {len(vars_missing_from_inputgens)}")
    print("\nList of all missing vars:")
    for v in vars_missing_from_inputgens:
        print(v)


def run_diagnostics():
    all_input_descs = check_inputgen_templates()
    check_deploygen_templates(all_input_descs)


# these are fields that do not appear in any template but that should nonetheless be in the
# input file (or start file) because they are utilized by deployer itsef. 
VALID_INPUT_FIELDS_NOT_IN_TEMPLATES = ['components_to_deploy', 'vault_url', ]

def run_input_check(input_file):
    """
    Main diagnostics function for an input file.
    """
    # make sure the input is valid yaml
    try:
        input_dict = yaml.safe_load(input_file)
    except Exception as e:
        print(f"Could not load yaml for file {input_file}. Is it valid YAML? Details: {e}")
        print("Cannot proceed with validation. Exiting...")
        return
    # make sure the input provided a components_to_deploy; if not, there isn't much we can do...
    components = input_dict.get('components_to_deploy')
    if not components:
        print(f"Did not find variable components_to_deploy in the input file. This field is required.")
        print("Cannot proceed with validation. Exiting...")
        return
    _, template_files = deployer.template_dirs_files('/deploygen/templates', components)
    required_vars = set()
    for t in template_files:
        result, error = get_vars_for_template(t)
        if not error:
            required_vars = required_vars.union(result)
        else:
            print(f"{bcolors.WARNING}Warning:{bcolors.ENDC} there were errors loading the template {t}; we are ignoring these variable in the diagnostic. Details: {error}")
    print(f"Checking for {len(required_vars)} variables for {len(components)} components.")
    print(f"Total variables provided in input file: {len(input_dict.keys())}.")
    found_error = False
    for v in required_vars:
        if v not in input_dict.keys():
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} required variable {v} is missing from the input file.")    
            found_error = True
    for v in input_dict.keys():
        if v not in required_vars and v not in VALID_INPUT_FIELDS_NOT_IN_TEMPLATES:
            print(f"{bcolors.WARNING}Warning:{bcolors.ENDC} input file included unrecognized variable: {v}")
    if not found_error:
        print("Validation passed, no missing variables detected.")

# ---------------
# Validators
# ---------------

def validate_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        print(f"Got non-200 response code from {url};\n code: {r.status_code};\ncontent: {r.content}")
        return False


def associate_site_services(site_id, user_dict):
    # the URL specified does not includes the site id.
    base_url = user_dict['primary_site_admin_tenant_base_url']
    url = f"{base_url}/v3/sites/{site_id}"
    print(f"looking up site {site_id} at {url}...")
    if validate_url(url):
        r = requests.get(url)
        try:
            output = r.json()["result"]
            service_list = output["services"]
            user_dict["services"] = service_list
            site_admin_tenant_id = output["site_admin_tenant_id"]
            user_dict["site_admin_tenant_id"] = site_admin_tenant_id
            url_split = url.split("/")
            user_dict["site_id"] = url_split[-1]
            url_split = url.split("/v3")
            user_dict["site_url"] = url_split[0]
            print(f"Retrieved the following data: \nAdmin tenant id for your site: {site_admin_tenant_id}\nService list: {service_list}\n")
        except Exception as e:
            print(f"Unable to parse output from {url}; \nDebug data: {e}. \nResponse content: {r.content}\nExiting...")
            return False
    else:
        print("Exiting...")
        return False
    # look up tenants associated with the site
    url = f"{base_url}/v3/tenants"
    user_dict['site_tenants'] = []
    r = requests.get(url)
    try:
        output = r.json()["result"]
        for tenant in output:
            if tenant['site_id'] == site_id:
                user_dict['site_tenants'].append(tenant['tenant_id'])
    except Exception as e:
        print(f"Unable to parse output from {url}; \nDebug data: {e}. \nResponse content: {r.content}\nExiting...")
        return False
    print(f"Found the following tenants: {user_dict['site_tenants']}")
    while True:
        choice = input(f"Do you want to: 1) use the above list of tenants or 2) enter your own list? Enter 1 or 2: ")
        if choice not in ['1', '2']:
            print("Invalid option; please enter 1 or 2...")
            continue
        break

    if choice == '2':
        done = False
        while not done:
            tenants_str = input("Enter the list of tenants as a JSON list (i.e., '[\"tenant_1\", \"tenant_2\"]'): ")
            try:
                if tenants_str == '_QUIT':
                    done = True
                    break                    
                tenants = json.loads(tenants_str)
                tp = type(tenants)
                if tp == list:
                    done = True
                    user_dict['site_tenants'] = tenants  
                else:
                    print(f"Invalid format; got type {tp} when deserializing the JSON; it should be a list.")
            except Exception as e:
                print(f"Invalid format; got exception trying to deserialize the JSON. details: {e}.")

    return True


# ----------------------------
# Data to gather from user
# ----------------------------

prompts = {
    "primary_site":
    {
        "template": "input_template.j2",
        "number": 1,
        "first_prompts": 
        {
            "primary_site_admin_tenant_base_url" : 
            {
                "regex": r"\w",
                "description": "Please enter the base URL for the primary site",
                "example": "https://admin.test.tapis.io",
            },
            "vault_external":
            {
                "regex": r"\w",
                "description": "Please indicate whether you will be using an external Vault, already installed and configured.",
                "example": "True"
            },
            "vault_url": 
            {
                "regex": r"\w",
                "description": "Enter a URL for the vault server",
                "example": "http://vault:8200"
            },
        },
        "second_prompts":{
            # TODO -- is there a choice on admite site id or is it hard-coded to "tacc" in the tenants table?
            "site_id" :
            {
                "regex": r"\w",
                "description": "Please enter the site_id",
                "example": "tacc"
            },
            # TODO -- i think this has to always be admin... no choice?
            "site_admin_tenant_id": 
            {
                "regex": r"\w",
                "description": "Please enter the tenat id for the admin tenant of this site (should be admin)",
                "example": "admin"
            },
            "site_tenants": 
            {
                "regex": r'\[("\w*"\,\s?)+("\w*")\]',
                "description": "Please enter an array of tenants to initialize the primary site with.",
                "example": '["dev", "admin"]'
            },
        }        
    },
    "associate_site":
    {
        "template": "associate_template.j2",
        "number": 2,
        "first_prompts": 
        {
            "primary_site_admin_tenant_base_url" :
            {
                "regex":  r"\w",
                "description": "Please enter the base URL of the admin tenant for the primary site",
                "example": "https://admin.test.tapis.io"
                
            },
            "site_id":
            {
                "regex": r"\w",
                "description": "Please enter the site id for your associate site.",
                "example": "assoc",
                "function": associate_site_services
            },
            "vault_external":
            {
                "regex": r"\w",
                "description": "Please indicate whether you will be using an external Vault, already installed and configured.",
                "example": "True"
            },
            "vault_url": 
            {
                "regex": r"\w",
                "description": "Enter a URL for the vault server",
                "example": "http://vault:8200"
            },
        },
        "second_prompts":{            
        }        
    },
    "common_second_prompts":
    {
            "tapis_image_version":
            {
                "regex": r"\w",
                "description": "Please enter the image version to deploy for all Tapis service containers.",
                "example": '["latest", "1.0.0", "dev"]'
            },
            "tapis_storage_class":
            {
                "regex": r"\w",
                "description": "Please enter the Kubernete storage class to use for all Tapis PVCs.",
                "example": "rbd",
            },
            "tapis_log_level":
            {
                "regex": r"\w",
                "description": "Please enter a log level to use for all Tapis services.",
                "example": "DEBUG"
            },
            "tapis_show_traceback":
            {
                "regex": r"\w",
                "description": "Whether to show the full (Python) traceback in logs.",
                "example": "true",
            },
            "tapis_python_api_processes":
            {
                "regex": r"\w",
                "description": "The number of Python processes to use for all Tapis Python API servers.",
                "example": 3
            },
            "tapis_python_api_threads":
            {
                "regex": r"\w",
                "description": "The number of Python threads (per process) to use for all Tapis Python API servers.",
                "example": 4
            },



    }
}


def parse_agrs():
    """
    Parse the arguments to the inputget program; returns the following fields for use later in the program:
    * out_dir (str) -- Path to a directory to write output. 
    * start_dict (dict) -- Dictionary of fields coming from the start_file option. 
    * long_prompt (bool) -- Whether to prompt the user for all possible prompts (default is true, overwritten with --min).
    * diagnostics (bool) -- Whether inputgen is running diagnostics on itself.
    * input_check (bool) -- Whether inputgen is running in a diagnostics mode to check an input file.
    * input_file (FileType) -- Path to the input file to check. Only set when input_check is true.
    """
    parser = argparse.ArgumentParser(description="Generate an input.yml file for deployer to use to generate deployments scripts.")
    parser.add_argument('-o', '--out', type=str, dest='out_dir', metavar='out_dir', nargs='?',
                        help="Directory to write program output; if not specified, this program will default to writing output to the current working directory.")
    parser.add_argument('-s', '--start', type=str, dest='start_file', metavar='start_file', nargs='?',
                        help="Location to a start file to seed this program with inputs. If provided, this program will use any values provided in the start file instead of prompting you for an input.")
    parser.add_argument('-m', '--min', action="store_true", help="Only prompt for a minimal number of prompts. This option generally will not result in a working input file.")
    parser.add_argument('-i', '--inputcheck', action="store_true", help="Run diagnostics on an inpute file. NOTE: Input generation is not performed in this mode.")
    parser.add_argument('-f', '--inputfile', type=argparse.FileType('r'), dest='input_file', help="An inpute file to run diagnostics on. This field is required when setting -i (--inputcheck) is ignored otherwise.")
    parser.add_argument('-d', '--diagnostics', action="store_true", help="Run diagnostics on inputgen itself. NOTE: Input generation is not performed in this mode.")
    parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose output.")
    args = parser.parse_args()
    global vb
    # defaults -----
    out_dir = ""
    start_dict = {}
    input_check = False
    input_file = ""
    long_prompt = True
    diagnostics = False
    
    if args.inputcheck:
        input_check = True
        input_file = args.input_file
        if not input_file:
            print("No input file specifed; an input file is required for inputcheck mode. Exiting...")
            sys.exit(1)
        print(f"running inputcheck for input file {input_file}; input generation will not be performed...")
        return out_dir, start_dict, long_prompt, diagnostics, input_check, input_file
    if args.diagnostics:
        diagnostics = True
        print("Running inputgen diagnostics; input generation will not be performed...")
    if vb: print(f"DEBUG: {args}")
    out_dir = args.out_dir
    if out_dir:
        print(f"output will be written to: {out_dir}")
    else:
        print("no output directory provided; output will be written to the cwd.")
    # options related to input generation are not relevant for diagnostics modes ---
    if diagnostics:
        if input_check:
            print("Please specify only one of --inputcheck and --diagnostics. Existing...")
            sys.exit(1)
        return out_dir, start_dict, long_prompt, diagnostics, input_check, input_file
    
    start_file = args.start_file
    if start_file:
        print(f"Using start file: {start_file}")
        # check that file exists and is in yaml format
        with open(start_file, 'r') as f:
            start_dict = yaml.safe_load(f.read()) 
    else:
        print("no start file; starting from the beginning.")   
    long_prompt = True
    if args.min:
        long_prompt = False
    if args.verbose:
        vb = True
    return out_dir, start_dict, long_prompt, diagnostics, input_check, input_file


def load_descs(components):
    """
    Returns the input descriptions contained within the input descriptions directory for all components in the 
    list of `components`.
    """
    all_input_descs = {}
    print(f"components to check: {components}")
    for f_name in os.listdir(INP_DESCS_DIR):
        # the file names are of the form { component }_desc.yml, so we can skip files that do not correspond to compoenents we are
        # generating
        comp = f_name.split('_')[0]
        if comp not in components:
            if vb: print(f'DEBUG: skipping component {comp} as it is not in the list of components to generate.')
            continue
        # each file should be a yaml file
        if vb: print(f'DEBUG: including {comp}')
        with open(os.path.join(INP_DESCS_DIR, f_name), 'r') as f:
            d = f.read()
            if d:
                all_input_descs.update(yaml.safe_load(d))
    return all_input_descs


def load_defaults():
    """
    Loads the inputgen default values; these are used for all input description that specify a default variable
    attribute.
    """
    DEFAULTS_FILE = '/inputgen/defaults.yml'
    with open(DEFAULTS_FILE, 'r') as f:
        return yaml.safe_load(f.read()) 


def determine_primary_or_assoc(start_dict, current_start_dict):
    """
    Prompt the user to specify whether they are deploying a primary or associate site.
    """
    ct = 0
    print(f"Found these keys in the start file: {start_dict.keys()}")
    while True:
        ct += 1
        # first time through, check it site_type was provided in the start file.
        if "site_type" in start_dict.keys() and ct == 1:
            inp = start_dict['site_type']
        else:
            inp = input("Will you be deploying a primary site or an associate site?\nEnter 1 for primary, 2 for associate: ")
        try:
            site_type = int(inp)
        except:
            print("Invalid input; please enter 1 or 2.\n")
            continue
        for key in prompts:
            if site_type == prompts[key]["number"]:
                site_prompts = prompts[key]
                if site_type == 1:
                    print("\nPlease enter the following additional information for generating a primary site config.")
                else:
                    print("\nPlease enter the following additional information for generating an associate site config.")
                current_start_dict["site_type"] = site_type
                return site_type, site_prompts, current_start_dict
        print("Input did not match any valid option; please enter 1 or 2.\n")


def extend_prompts_with_inputs(second_prompts, all_input_descs):
    """
    Add a prompt for each input description if the input specifies exactly one source var which is itself.
    That is, an input will *not* be added as a prompt if it specifies a different source var which would allow
    it to be derived from some other variable. 
    """
    for var, desc in all_input_descs.items():
        # make sure the description has a source_vars
        if 'source_vars' not in desc:
            continue
        # if there is exactly one source var and it has the same name as the var itself, add it to the prompts
        if len(desc['source_vars']) == 1 and desc['source_vars'][0] == var:
            second_prompts[var] = desc
    return second_prompts


def collect_user_dict(prompts, prev_start_dict, current_start_dict, user_dict, defaults):
    """
    Runs a set of interactive prompts to solicit input from the user. 
    """
    for key, value in prompts.items():
        user_input = ""
        match = False
        validate = False
        quit_early = False
        ct = 0
        while True:
            ct = ct + 1
            description = value.get("description")
            if not description:
                print(f"ERROR: field {key} missing description field. Deployer should be updated!")
                if vb: print(f"keys on value: {value.keys()}")
                description = "(not provided)"
            main_prompt = f"({key}) " + description
            default_var_name = value.get('default')
            if default_var_name:
                # look up the default value
                default_value = defaults.get(default_var_name)
                if not default_value:
                    print(f"ERROR: field {key} specified a default variable of {default_var_name} but no default value was provided.\
                            Deployer needs to be updated!")
                else:
                    # add the default to the prompt:
                    main_prompt = main_prompt + f" (default value: {default_value})"
            
            example = value.get("example", "No example provided.")
            # look for the variable in the previous start dictionary and use that if it is present
            if ct == 1 and key in prev_start_dict:
                user_input = prev_start_dict[key]
                if vb: print(f"DEBUG: using start file for input {key}; attempting to use value {user_input}.")
            # if the variable was not in the previous start dict, prompt the user to input the value
            else:
                user_input = input(f"{main_prompt} (Example: {example}): ")
            # parse the user's input --------
            # look for special quit command
            if user_input == '_QUIT':
                print("quiting...")
                quit_early = True
                return user_dict, current_start_dict, quit_early
            # check if the prompt specified a regex validator, and if it did, use that to validate the input
            regex = value.get("regex")
            if regex:
                if (re.match(regex, user_input)):
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}

### Everything first goes through this stream stanza. Map matches subdomain to port to route to.
### If no map found, we route to default 8443. This directs back to HTTP stanza as normal.
stream {

    log_format stream_routing '$remote_addr [$time_local] '
                              'with SNI name "$ssl_preread_server_name" '
                              'proxying to "$instanceport" '
                              '$protocol $status $bytes_sent $bytes_received '
                              '$session_time';

    # 'map' maps input string to output variable. Regex works.
    # Ports used are purely random. Feel free to change.
    map $ssl_preread_server_name $instanceport {
        # Route TCP with following whatever.pods.whatever.develop.tapis.ioto pods-nginx.
        "~pods.*.develop.tapis.io"      5510;
        # Else default to 8443 (listened to by http stanza).
        default                         8443;
    }
 
    # pods_service. Route TCP to pods-nginx pod.
    server {
        listen                 5510;
        ssl_preread            off;
        proxy_timeout          600s;
        access_log /dev/stdout stream_routing;
    {%- if "pods" in proxy_nginx_service_list %}
        proxy_pass             pods-nginx:80;
    {%- else %}
        # cgarcia- Unsure if this entire 'server' block should be in an if, or if we
        # should what I'm doing here.
        proxy_pass             {{proxy_primary_site_admin_tenant_base_url}};
    {%- endif %}        

    }

    # Listen for all incoming requests. Preread server name (for mapping). Then pass. 
    server {
        listen                  443;
        ssl_preread             on;
        proxy_connect_timeout   20s;  # max time to connect to pserver
        proxy_timeout           600s;
        access_log /dev/stdout stream_routing;
        proxy_pass              127.0.0.1:$instanceport;
    }
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    # hammock 20211112
    log_format  main  '$remote_addr - $remote_user [$time_local] "$host" "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';


    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    # Redirect all non-encrypted traffic to the encrypted site.
    server
    {
        listen 80;
        listen [::]:80;
    
        server_name  {{proxy_nginx_server_name}};
    
        # Redirect with 307 to preserve post data. (301 does not)
        if ($request_method = POST) {
            return 307 https://$server_name$request_uri;
        }
    
        # Permanent redirect to the secured site.
        return 301 https://$server_name$request_uri;
    }

    # Configuration for the encrypted site.
    server
    {
    
        listen 8443 ssl http2;
        listen [::]:8443 ssl http2;
    
        server_name  {{proxy_nginx_server_name}};
    
        ssl_certificate /tmp/ssl/tls.crt;
        ssl_certificate_key /tmp/ssl/tls.key;
    
        # SSL configs. Do not change.
        ssl_session_timeout 1d;
        ssl_session_cache shared:MozSSL:10m;
        ssl_session_tickets off;
        ssl_protocols TLSv1.2;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        add_header Strict-Transport-Security "max-age=63072000" always;
        ssl_stapling on;
        ssl_stapling_verify on;
    
        charset utf-8;
        keepalive_timeout 5;
    
        #CORS support
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, PATCH, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Mx-ReqToken,X-Requested-With,x-tapis-token' always;
    
        # big upload support
        proxy_connect_timeout 3600;
        proxy_send_timeout    3600;
        proxy_read_timeout    3600;
        send_timeout          3600;
    
	# authenticator
        location /v3/oauth2
        {
    #        auth_request /_auth;
        {%- if "authenticator" in proxy_nginx_service_list %}
            proxy_pass http://authenticator-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $remote_addr;
    
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Allow-Credentials' 'true';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, PATCH, DELETE, OPTIONS';
                add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Mx-ReqToken,X-Requested-With,x-tapis-token';
                return 204;
            }    
        }

	# site-router
        location /v3/site-router
        {
           # this location intentionally does NOT get an auth_request directive since the site-router endpoints IS the target of auth_request.
           proxy_pass http://site-router-api:8000;
           proxy_redirect off;
           proxy_set_header Host $host;
        }
        
	# security 
        location /v3/security
        {
    #        auth_request /_auth;
        {%- if "security" in proxy_nginx_service_list %}
            proxy_pass http://sk-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
        } 

	# tenants 
        location /v3/tenants
        {
            # auth_request /_auth;
        {%- if "tenants" in proxy_nginx_service_list %}
            proxy_pass http://tenants-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host localhost:5000;
        }

	# _auth
        location /_auth {
            internal;
           
            # check to see if either of the x-tapis-tenant or x-tapis-user are set then return 200
            set $x_tenant $http_x_tapis_tenant;
            set $x_user $http_x_tapis_user;
            if ($x_tenant){
              return 200;
            }
    
            if ($x_user){
              return 200;
            }
    
            # if $token is not set (i.e., if x-tapis-token was sent) then return 200
            set $token $http_x_tapis_token;
            if ($token ~ "^$") {
              return 200; 
            }
            proxy_method GET;
            proxy_set_header X-Tapis-Token $http_x_tapis_token;
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}}/v3/site-router/check;
        }
    
	# sites
        location /v3/sites
        {
    #        auth_request /_auth;
        {%- if "tenants" in proxy_nginx_service_list %}
            proxy_pass http://tenants-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host localhost:5000;
        }
        
	# meta
        location /v3/meta
        {
    #        auth_request /_auth;
        {%- if "meta" in proxy_nginx_service_list %}
            proxy_pass http://restheart-security:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
        }
        
	# streams
        location /v3/streams
        {
    #        auth_request /_auth;
        {%- if "streams" in proxy_nginx_service_list %}
            proxy_pass http://streams-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $remote_addr;
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Allow-Credentials' 'true';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, PATCH, DELETE, OPTIONS';
                add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Mx-ReqToken,X-Requested-With,x-tapis-token';
                return 204;
            }
        }
        
	# files
        location /v3/files
        {
    #        auth_request /_auth;
        {%- if "files" in proxy_nginx_service_list %}
            proxy_pass http://files-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
            client_max_body_size 50G;
        }

	# systems
        location /v3/systems
        {
    #        auth_request /_auth;
        {%- if "systems" in proxy_nginx_service_list %}
            proxy_pass http://systems-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
        }

	# tokens
        location /v3/tokens
        {
            # we intentionally do NOT include an auth_request for Tokens because tokens only handles service requests.
        {%- if "tokens" in proxy_nginx_service_list %}
            proxy_pass http://tokens-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host localhost:5000;
        }

	# jobs
        location /v3/jobs
        {
    #        auth_request /_auth;
        {%- if "jobs" in proxy_nginx_service_list %}
            proxy_pass http://jobs-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}
            proxy_redirect off;
            proxy_set_header Host $host;
        }

	# actors 
        location /v3/actors
        {
    #        auth_request /_auth;
        {%- if "actors" in proxy_nginx_service_list %}
            proxy_pass http://actors-nginx:80;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }
    # pods
        location /v3/pods
        {
        {%- if "pods" in proxy_nginx_service_list %}
            proxy_pass http://pods-nginx:80;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }


	# apps
        location /v3/apps
        {
    #        auth_request /_auth;
        {%- if "apps" in proxy_nginx_service_list %}
            proxy_pass http://apps-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }

	# monitoring
        location /grafana/
        {
        {%- if "monitoring" in proxy_nginx_service_list %}
            proxy_pass http://monitoring-grafana:3000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }

	# pgrest
        location /v3/pgrest
        {
    #        auth_request /_auth;
        {%- if "pgrest" in proxy_nginx_service_list %}
            proxy_pass http://pgrest-api:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
            # This is some pgrest shenanigans to get the a2cps tenant doing it's stuff. Ask Christian Garcia.
            if ($host = 'a2cps.tapis.io') {
                proxy_pass http://c009.rodeo.tacc.utexas.edu:30076;
            }
            if ($host = 'a2cpsdev.tapis.io') {
                proxy_pass http://c009.rodeo.tacc.utexas.edu:32379;
            }
        }

	# notifications
        location /v3/notifications
        {
    #        auth_request /_auth;
        {%- if "notifications" in proxy_nginx_service_list %}
            proxy_pass http://notifications-api:8080;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }

	# globus-proxy
        location /v3/globus-proxy
        {
        {%- if "globus-proxy" in proxy_nginx_service_list %}
            proxy_pass http://globus-proxy:5000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }

    # workflows
        location /v3/workflows
        {
        {%- if "workflows" in proxy_nginx_service_list %}
            proxy_pass http://workflows-api-service:8000;
        {%- else %}
            proxy_pass {{proxy_primary_site_admin_tenant_base_url}};
        {%- endif %}        
            proxy_redirect off;
            proxy_set_header Host $host;
        }

    }
}

                    match = True
                else:
                    print(f"Input ({user_input}) did not match expected format.\n")
            else:
                match = True
            # if the prompt specifed a function, we call it to validate the input.
            # the function should return a tuple containing a bool and a value; 
            #   - bool should be true if the value validated and false if not.
            #   - value should be the value to use.
            if ("function" in value):
                try:
                    validate = value["function"](user_input, user_dict)
                except Exception as e:
                    print(f"Validate Function failed. Additional info: {type(e)}: {e}\n")
                    print(e)
            else:
                validate = True
            if(match and validate):
                if(type(validate) == tuple):
                    user_dict[key] = validate[1]
                else:
                    user_dict[key] = user_input
                # add the key to the current start file either way
                current_start_dict[key] = user_dict[key]
                print("\n")
                break
    return user_dict, current_start_dict, quit_early


def compute_components_to_deploy(user_dict):
    # all sites get the following components
    components = set(['admin', 
                    'authenticator', 
                    'container-registry', 
                    'monitoring', 
                    'proxy', 
                    'security', 
                    'skadmin', 
                    'tokens',])
    # vault could be in k8s or external -
    if not user_dict['vault_external'].lower == 'true':
        components.add('vault')
    # primary sites get all remaining components:
    if user_dict['site_type'] == 1:
        components = components.union(['actors', 'apps', 'files', 'jobs', 'notifications', 
        'pgrest', 'pods', 'streams', 'systems', 'tenants'])
    # associate sites get components corresponding to the services they are deploying:
    else:
        print(f"components for associate site: {user_dict['services']}")
        components = components.union(user_dict['services'])
        print(F"FINAL component list: {components}")
    return list(components)


def compute_inputs(all_input_descs, user_dict, defaults):
    """
    Computes a dictionary of "inputs" using the input descriptions, defaults and the dictionary of user-provided
    values.
      * all_input_descs - the dict of input descriptions.
      * user_dict - the dict of user-provided values collected via the prompts and start file.
      * defaults - the default values provided by deployer for the inputs.
    """
    # actual result to return; always add the site_type
    site_type = user_dict.get("site_type")
    if not site_type:
        print("Error: site_type was missing from the set of all values derived from the user-supplied values. This should never happen.")
    inputs = {"site_type": site_type}

    # 

    # iterate over every input defined in the input descriptions dictionary -----
    for inp, desc in all_input_descs.items():
        if vb: print(f"DEBUG: processing input: {inp}")
        found = False
        # some variables CANNOT be changed via deployer; they have a value specified in the description that must be used.
        # examples include fields like the service name (e.g., apps_service_name)
        if 'value' in desc.keys():
            value = desc.get('value')
            inputs[inp] = value
            found = True
            continue
        try:
            source_vars = desc['source_vars']
        except:
            print(f"{bcolors.FAIL}\n***** ERROR: Invalid input description for input {inp}. No source_vars defined. ***** \n{bcolors.ENDC}")
            continue
        # variables can be set to "optional", meaning their existence does not impact the ability to compile the templates.
        optional = desc.get('optional', False)

        for s in source_vars:
            # look for the source var in the user_dict
            if s in user_dict.keys():
                # use the first source var that appears in the user_dict
                inputs[inp] = user_dict[s]
                found = True
                break
        # if we got through all the source_vars without finding a value, look to see if a default is allowed for this input
        else:
            # if an allowable default was specified, look for it in the defaults dict
            if 'default_var' in desc.keys():
                try:
                    inputs[inp] = defaults[desc['default_var']]
                    continue
                except:
                    pass
            # if the input declared itself to be optional or if we found a value, we can safely continue.
        if optional or found:
            continue
        # we never found the value, raise an error and get out...
        description = desc.get('description')
        example = desc.get('example')
        print(f"{bcolors.WARNING}\n***** Could not determine a value for the input {inp}. Please specify a value. ***** {bcolors.ENDC}")
        print(f"Source vars: {source_vars}")
        print(f"Supplied keys: {user_dict.keys()}")
        print(f"Description: {description}")
        print(f"Example: {example}\n\n")
        sys.exit(1)

    return inputs


def ensure_outdir(outDir):
    if outDir:
        outDir = outDir.strip()
        try:
            if vb: print(f"DEBUG: creating {outDir} if it does not exist.")
            test = outDir
            test2 = os.path.expanduser(test)
            os.makedirs(test2)
            return test2
        except:
            if vb: print(f"DEBUG: {outDir} already existed.")
            return outDir
    else:
        outdir = os.getcwd()
        print(f"using current working directory ({outdir})")
        return outdir


def write_start_file(current_start_dict, outDir):
    out_dir = ensure_outdir(outDir)
    file_path = os.path.join(os.path.abspath(out_dir), "start_file.yml")
    with open(file_path, 'w') as f:
        f.write(yaml.dump(current_start_dict, Dumper=NoAliasDumper))


def write_raw_input_file(inputs, outDir):
    out_dir = ensure_outdir(outDir)
    file_path = os.path.join(os.path.abspath(out_dir), "raw_inputs_file.yml")
    with open(file_path, 'w') as f:
        f.write(yaml.dump(inputs, Dumper=NoAliasDumper))
    print(f"output file written to: {file_path}")


# def write_output(preset, outDir, user_dict):
#     template = env.get_template(preset["template"])
#     out_dir = ensure_outdir(outDir)
#     file_path = os.path.join(os.path.abspath(out_dir), "input.yml")
#     with open(file_path, "w") as f:
#         f.write(template.render(user_params=user_dict))
#         print(f"output file generated to: {file_path}")


def exit():
    
    sys.exit(1)



def main():
    out_dir, prev_start_dict, long_prompt, diagnostics, input_check, input_file = parse_agrs()
    # diganostics mode is completely different and does not do input generation
    if diagnostics:
        run_diagnostics()
        sys.exit()
    # input_check mode is also completely different and does not do input generation
    if input_check:
        run_input_check(input_file)
        sys.exit()

    if long_prompt:
        print("Running with extended prompts")

    # we start the current start dict with the previous one..
    current_start_dict = prev_start_dict

    # load the provided defaults
    defaults = load_defaults()

    # determine whether we are deploying a primary or an associate site
    site_type, site_prompts, current_start_dict = determine_primary_or_assoc(prev_start_dict, current_start_dict)
    user_dict = {'site_type': site_type}
    if site_type == 1:
        user_dict['services'] = PRIMARY_SITE_SERVICES

    # prompt the user for inputs for the first set of prmopts; these prompts actually determine which components will be generated.
    user_dict, current_start_dict, quit_early = collect_user_dict(site_prompts["first_prompts"], prev_start_dict, current_start_dict, user_dict, defaults)

    if quit_early:
        # always write a start file that can be used for a subsequent run
        write_start_file(current_start_dict, out_dir)
        sys.exit("start file written.")
      
    # get all components needed for the site type
    components = compute_components_to_deploy(user_dict)
    if vb: print(f'DEBUG: need to generate the following components: {components}')
    # load the descriptions of all input fields we need to get values for; we only need values for the components we are generating
    all_input_descs = load_descs(components)

    # prompt the user for inputs for the second set of prmopts; at a minimum, draw prompts from both the site_type and common sets.
    second_prompts = {**prompts['common_second_prompts'], **site_prompts["second_prompts"]}
    # additionally, if long_prompt was specified, add prompts for every input that only specifies itself as a source_var
    if long_prompt:
        second_prompts = extend_prompts_with_inputs(second_prompts, all_input_descs)

    user_dict, current_start_dict, quit_early = collect_user_dict(second_prompts, prev_start_dict, current_start_dict, user_dict, defaults)
    
    # always write a start file that can be used for a subsequent run
    write_start_file(current_start_dict, out_dir)
    if quit_early:
        sys.exit("start file written.")

    inputs = compute_inputs(all_input_descs, user_dict, defaults)

    inputs['components_to_deploy'] = components
    # write the input.yml file as a "raw" yaml dump --
    # if vb: print(f"about to write input file; inputs key: {inputs.keys()}")
    if vb:
        print(f"about to write input file; all keys that are lists:")
        print(inputs['security_service_site_id'])
        # for k in inputs.keys():
        #     if type(inputs[k]) == list:
        #         print(k)
    write_raw_input_file(inputs, out_dir)


if __name__ == "__main__":
    main()
