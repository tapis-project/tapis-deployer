import re
import requests
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import argparse
import os

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader, undefined=StrictUndefined)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

user_dict = {}

def validate_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        print("Validate Function failed")
        print(r.text)
        return False

def associate_site_services(url):
    if validate_url(url):
        r = requests.get(url)
        output = r.json()
        output = output["result"]["services"]
        service_list = output
        user_dict["services"] = service_list
        url_split = url.split("/")
        user_dict["site_id"] = url_split[-1]
        url_split = url.split("/v3")
        user_dict["site_url"] = url_split[0]
        return True, output
    else:
        return False


prompts = {
    "main_deployment":
    {
        "template": "input_template.j2",
        "number": 1,
        "prompts": 
        {
            "site_url" : 
            {
                "regex": r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                "description": "Please enter the site_url",
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
            "main_site_url" :
            {
                "regex": r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                "description": "Please enter the site_url of the mainsite",
                "example": "https://admin.test.tapis.io/v3/sites/(site_id)",
                "function": associate_site_services
            },
            "tenant_id": 
            {
                "regex": r"\w",
                "description": "Please enter the associate site admin tenant id",
                "example": "assocadm"
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

def main():

    parser = argparse.ArgumentParser(description="Generate yaml config file")

    parser.add_argument('-o', dest='outDir', metavar='outDir', nargs='?',
                        help="File location of program output, if not specified defaults current location")

    args = parser.parse_args()

    while True:
        print("What preset would you like to use")
        for key in prompts:
            print(key, ":", str(prompts[key]["number"]), "\n")

        preset_num = int(input())

        for key in prompts:
            if preset_num == prompts[key]["number"]:
                preset = prompts[key]
                break
        if preset:
            break
        else:
            print("Input did not match any preset")

    for key, value in preset["prompts"].items():
        user_input = ""
        match = False
        validate = False
        while True:
            print(value["description"])
            print("Here is an example", value["example"] + ":\n")
            user_input = input()
            regex = value["regex"]
            if (re.match(regex, user_input)):
                match = True
            else:
                print("Input did not match expected format")
            if ("function" in value):
                try:
                    validate = value["function"](user_input)
                except Exception as e:
                    print("Validate Function failed")
                    print(e)
            else:
                validate = True
            if(match and validate):
                if(type(validate) == tuple):
                    user_dict[key] = validate[1]
                else:
                    user_dict[key] = user_input
                break
        
    template = env.get_template(preset["template"])
    outDir = args.outDir
    if(outDir):
        outDir = outDir.strip()
        try:
            test = outDir
            test2 = os.path.expanduser(test)
            os.makedirs(test2)
        except:
            pass
        with open(os.path.abspath(outDir)+"input.yml", "w") as file:
            file.write(template.render(user_params = user_dict))
    else:
        with open("input.yml", "w") as file:
            file.write(template.render(user_params = user_dict))

if __name__ == "__main__":
    main()
