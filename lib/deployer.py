import os
#from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2 import Environment, FileSystemLoader


def create_tapis(template_path, out_dir, input_data):
    '''
    Walk through the template directory and create Tapis deployment files from templates. 
    '''
    
    # jinja setup
    env = Environment(loader=FileSystemLoader('templates'))
    # env = Environment(loader=FileSystemLoader('templates'), undefined=StrictUndefined)  
    # todo: do we need this? 
    # env.trim_blocks = True
    # env.lstrip_blocks = True
    # env.rstrip_blocks = True

    for dirpath, dirnames, filenames in os.walk(template_path, topdown=False):
        # this if prevents exception when talking path and dirpath becomes empty
        if dirpath != template_path:
            relative_dirpath = dirpath[dirpath.index("/")+1:]
            # print(relative_dirpath)
            for filename in filenames:
                # template path
                tpath = os.path.join(relative_dirpath, filename)
                # dest file path
                destpath = os.path.join(out_dir, relative_dirpath, filename)
                print('templating {} to {}'.format(tpath, destpath))
                template = env.get_template(tpath)
                with open('{}'.format(destpath), "w") as file:
                    file.write(template.render(input_data))
                    

        

