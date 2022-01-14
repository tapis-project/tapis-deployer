import re
import requests
from jinja2 import Environment, FileSystemLoader
import argparse
import os

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True


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
    base_url = user_dict['primary_site_url']
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
        
        return True, output
    else:
        print("Exiting...")
        return False


# ----------------------------
# Data to gather from user
# ----------------------------

prompts = {
    "primary_site":
    {
        "template": "input_template.j2",
        "number": 1,
        "prompts": 
        {
            "site_url" : 
            {
                "regex": r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                "description": "Please enter the base URL for the primary site",
                "example": "https://admin.test.tapis.io",
            },
            "site_id" :
            {
                "regex": r"\w",
                "description": "Please enter the site_id",
                "example": "admin"
            },
            "tenants": 
            {
                "regex": r'\[("\w*"\,\s?)+("\w*")\]',
                "description": "Please enter an array of tenants",
                "example": '["dev", "admin"]'
            }
        }
    },
    "associate_site":
    {
        "template": "associate_template.j2",
        "number": 2,
        "prompts": 
        {
            "primary_site_url" :
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
            "tenants": 
            {
                "regex": r'\[("\w*"\,\s?)+("\w*")\]',
                "description": "Please enter an array of tenants",
                "example": '["assocadm", "assocdev"]'
            }
        }
    }
}


def parse_agrs():
    parser = argparse.ArgumentParser(description="Generate yaml config file")
    parser.add_argument('-o', dest='outDir', metavar='outDir', nargs='?',
                        help="File location of program output, if not specified defaults current location")
    args = parser.parse_args()
    outDir = args.outDir
    if outDir:
        print(f"output will be written to: {outDir}")
    else:
        print("no output directoty provided; output will be written to the cwd.")
    return outDir


def determine_primary_or_assoc():
    while True:
        inp = input("Will you be deploying a primary site or an associate site?\nEnter 1 for primary, 2 for associate: ")
        try:
            preset_num = int(inp)
        except:
            print("Invalid input; please enter 1 or 2.\n")
            continue
        for key in prompts:
            if preset_num == prompts[key]["number"]:
                preset = prompts[key]
                if preset_num == 1:
                    print("\nPlease enter the following additional information for generating a primary site config.")
                else:
                    print("\nPlease enter the following additional information for generating an associate site config.")
                return preset
        print("Input did not match any valid option; please enter 1 or 2.\n")


def collect_user_dict(preset):
    user_dict = {}
    for key, value in preset["prompts"].items():
        user_input = ""
        match = False
        validate = False
        while True:
            main_prompt = value["description"]
            example = value["example"]
            user_input = input(f"{main_prompt} (Example: {example}): ")
            regex = value["regex"]
            if (re.match(regex, user_input)):
                match = True
            else:
                print("Input did not match expected format.\n")
            if ("function" in value):
                try:
                    validate = value["function"](user_input, user_dict)
                except Exception as e:
                    print("Validate Function failed.\n")
                    print(e)
            else:
                validate = True
            if(match and validate):
                if(type(validate) == tuple):
                    user_dict[key] = validate[1]
                else:
                    user_dict[key] = user_input
                print("\n")
                break
    return user_dict


def write_output(preset, outDir, user_dict):
    template = env.get_template(preset["template"])
    if outDir:
        outDir = outDir.strip()
        try:
            print(f"DEBUG: creating {outDir} if it does not exist.")
            test = outDir
            test2 = os.path.expanduser(test)
            os.makedirs(test2)
        except:
            print(f"DEBUG: {outDir} already existed.")
        
        file_path = os.path.join(os.path.abspath(outDir), "input.yml")
        with open(file_path, "w") as f:
            f.write(template.render(user_params=user_dict))
            print(f"output file generated to: {file_path}")
    else:
        with open("input.yml", "w") as file:
            file.write(template.render(user_params=user_dict))
            print("output file generated to input.yml in current working directory.")


def main():
    outDir = parse_agrs()
    preset = determine_primary_or_assoc()
    user_dict = collect_user_dict(preset)
    write_output(preset, outDir, user_dict)
        

if __name__ == "__main__":
    main()