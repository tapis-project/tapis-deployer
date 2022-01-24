import re
import requests
from jinja2 import Environment, FileSystemLoader
import argparse
import os
import sys
import yaml

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

# whether to print verbose output
vb = False


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


PRIMARY_SITE_SERVICES = ["actors", "apps", "authenticator", "files", "jobs", "meta", "monitoring", 
"notifications", "pgrest", "security", "streams", "systems", "tenants", "tokens"]


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
    return True, output


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
                "regex": r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                "description": "Please enter the base URL for the primary site",
                "example": "https://admin.test.tapis.io",
            },
            "vault_external":
            {
                "regex": r"\w",
                "description": "Please indicate whether you will be using an external Vault, already installed and configured.",
                "example": "True"
            }            
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
            "vault_url": 
            {
                "regex": r"\w",
                "description": "Enter a URL for the vault server",
                "example": "http://vault:8200"
            },
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
    },
    "associate_site":
    {
        "template": "associate_template.j2",
        "number": 2,
        "first_prompts": 
        {
            "primary_site_admin_tenant_base_url" :
            {
                "regex": r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
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
            }
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
                "regex": f"\w",
                "description": "Please enter the Kubernetes storage class to use for persistent volume claims (PVCs).",
                "example": "rbd-new"
            }

    }
}


def parse_agrs():
    parser = argparse.ArgumentParser(description="Generate an input.yml file for deployer to use to generate deployments scripts.")
    parser.add_argument('-o', '--out', type=str, dest='outDir', metavar='outDir', nargs='?',
                        help="Directory to write program output; if not specified, this program will default to writing output to the current working directory.")
    parser.add_argument('-s', '--start', type=str, dest='start_file', metavar='start_file', nargs='?',
                        help="Location to a start file to seed this program with inputs. If provided, this program will use any values provided in the start file instead of prompting you for an input.")
    parser.add_argument('-l', '--lprompt', action="store_true", help="Prompt for all missing configs.")
    parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose output.")
    args = parser.parse_args()
    global vb
    if vb: print(f"DEBUG: {args}")
    outDir = args.outDir
    if outDir:
        print(f"output will be written to: {outDir}")
    else:
        print("no output directoty provided; output will be written to the cwd.")
    start_file = args.start_file
    start_dict = {}
    if start_file:
        # check that file exists and is in yaml format
        with open(start_file, 'r') as f:
            start_dict = yaml.safe_load(f.read()) 
    else:
        print("no start file; starting from the beginning.")   
    long_prompt = False
    if args.lprompt:
        long_prompt = True
    if args.verbose:
        vb = True
    return outDir, start_dict, long_prompt


def load_descs(components):
    INP_DESCS_DIR = '/inputgen/inputdescs'
    all_input_descs = {}
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
    DEFAULTS_FILE = '/inputgen/defaults.yml'
    with open(DEFAULTS_FILE, 'r') as f:
        return yaml.safe_load(f.read()) 


def determine_primary_or_assoc(start_dict, current_start_dict):
    ct = 0
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
    for var, desc in all_input_descs.items():
        # make sure the description has a source_vars
        if 'source_vars' not in desc:
            continue
        # if there is exactly one source var and it has the same name as the var itself, add it to the prompts
        if len(desc['source_vars']) == 1 and desc['source_vars'][0] == var:
            second_prompts[var] = desc
    return second_prompts


def collect_user_dict(prompts, prev_start_dict, current_start_dict, user_dict):
    for key, value in prompts.items():
        user_input = ""
        match = False
        validate = False
        quit_early = False
        ct = 0
        while True:
            ct = ct + 1
            main_prompt = f"({key}) " + value["description"]
            example = value.get("example", "No example provided.")
            if ct == 1 and key in prev_start_dict:
                user_input = prev_start_dict[key]
                if vb: print(f"DEBUG: using start file for input {key}; attempting to use value {user_input}.")
            else:
                user_input = input(f"{main_prompt} (Example: {example}): ")
            # look for special quit command
            if user_input == '_QUIT':
                print("quiting...")
                quit_early = True
                return user_dict, current_start_dict, quit_early

            regex = value.get("regex")
            if regex:
                if (re.match(regex, user_input)):
                    match = True
                else:
                    print(f"Input ({user_input}) did not match expected format.\n")
            else:
                match = True
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
                current_start_dict[key] = user_input
                print("\n")
                break
    return user_dict, current_start_dict, quit_early


def compute_components_to_deploy(user_dict):
    # all sites get the following components
    components = ['admin', 'authenticator', 'container-registry', 'monitoring', 'proxy', 'security', 'skadmin', 'tokens',]
    # vault could be in k8s or external -
    if not user_dict['vault_external'].lower == 'true':
        components.append('vault')
    # primary sites get all remaining components:
    if user_dict['site_type'] == 1:
        components.extend(['actors',  'apps', 'files', 'jobs', 'notifications', 
        'pgrest',  'streams', 'systems', 'tenants'])
    # associate sites get components corresponding to the services they are deploying:
    else:
        components.extend(user_dict['services'])    
    return components


def compute_inputs(all_input_descs, user_dict, defaults):
    inputs = {}
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
            sys.exit(1)
        # variables can be set to "optional", meaning their existence does not impact the ability to compile the templates.
        # TODO -- need to implement optional below...
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
        if found:
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
        f.write(yaml.dump(current_start_dict))


def write_raw_input_file(inputs, outDir):
    out_dir = ensure_outdir(outDir)
    file_path = os.path.join(os.path.abspath(out_dir), "raw_inputs_file.yml")
    with open(file_path, 'w') as f:
        f.write(yaml.dump(inputs))


def write_output(preset, outDir, user_dict):
    template = env.get_template(preset["template"])
    out_dir = ensure_outdir(outDir)
    file_path = os.path.join(os.path.abspath(out_dir), "input.yml")
    with open(file_path, "w") as f:
        f.write(template.render(user_params=user_dict))
        print(f"output file generated to: {file_path}")


def main():
    outDir, prev_start_dict, long_prompt = parse_agrs()
    # we start  the current start dict with the previous one..
    current_start_dict = prev_start_dict
    
    # determine whether we are deploying a primary or an associate site
    site_type, site_prompts, current_start_dict = determine_primary_or_assoc(prev_start_dict, current_start_dict)
    user_dict = {'site_type': site_type}
    if site_type == 1:
        user_dict['services'] = PRIMARY_SITE_SERVICES

    # prompt the user for inputs for the first set of prmopts; these prompts actually determine which components will be generated.
    user_dict, current_start_dict, quit_early = collect_user_dict(site_prompts["first_prompts"], prev_start_dict, current_start_dict, user_dict)

    if quit_early:
        # always write a start file that can be used for a subsequent run
        write_start_file(current_start_dict, outDir)
        sys.exit("start file written.")
      
    # get all components needed for the site type
    components = compute_components_to_deploy(user_dict)
    if vb: print(f'DEBUG: need to generate the following components: {components}')
    # load the descriptions of all input fields we need to get values for; we only need values for the components we are generating
    all_input_descs = load_descs(components)
    # load the provided defaults
    defaults = load_defaults()

    # prompt the user for inputs for the second set of prmopts; at a minimum, draw prompts from both the site_type and common sets.
    second_prompts = {**prompts['common_second_prompts'], **site_prompts["second_prompts"]}
    # additionally, if long_prompt was specified, add prompts for every input that only specifies itself as a source_var
    if long_prompt:
        second_prompts = extend_prompts_with_inputs(second_prompts, all_input_descs)

    user_dict, current_start_dict, quit_early = collect_user_dict(second_prompts, prev_start_dict, current_start_dict, user_dict)
    
    # always write a start file that can be used for a subsequent run
    write_start_file(current_start_dict, outDir)
    if quit_early:
        sys.exit("start file written.")

    inputs = compute_inputs(all_input_descs, user_dict, defaults)

    inputs['components_to_deploy'] = components
    # write the input.yml file as a "raw" yaml dump --
    write_raw_input_file(inputs, outDir)


if __name__ == "__main__":
    main()