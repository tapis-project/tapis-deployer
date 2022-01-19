import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined

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
                    
def mkdir_if_missing(dir):
    '''
    Create dir if it does not exist
    '''
    if not os.path.exists(dir):
        os.mkdir(dir)

def copy_dir_tree(template_dir, dest_dir_base, exclude_subdirs=[]):
    '''
    Walk through the template directory and create Tapis deployment files from templates. 
    Skip the dirs/components in "exclude" list.
    '''

    # recreate template dir directory structure recursively

    template_dirs = [dest_dir_base]

    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(template_dir)):
        for d in dirnames:
            #print(os.path.join(dirpath,d))
            template_dirs.append(os.path.join(dirpath,d))

    for i in template_dirs:
        # replace template path with dest_dir_base
        dest_dir = str(i).replace(template_dir, dest_dir_base)
        # debug
        print('{} -> {}'.format(i,dest_dir))
        mkdir_if_missing(dest_dir)

def copy_files_tree(template_dir, dest_dir_base, input_data, exclude_subdirs):
    '''
    Walk through the template directory and create Tapis deployment files from templates. 
    Skip the dirs/components in "exclude" list.
    '''

    template_files = []

    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(template_dir)):
        for f in filenames:
            #print(os.path.join(dirpath,f))
            template_files.append(os.path.join(dirpath,f))

    for i in template_files:
        # replace template path with dest_dir_base
        dest_file = str(i).replace(template_dir, dest_dir_base)
        # remove template_dir path prefix from i
        relative_i = str(i).replace(template_dir, '')
        # debug
        #print('{} -> {}'.format(i,dest_file))
        apply_template(template_dir, relative_i, dest_file, input_data)


def jinjatest(input_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("burnup")
    print(template.render(input_data))

#template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('mydir'))
#template_env.get_template('foo/bar.html')

def apply_template(template_dir, src_file, dest_file, input_data=None):
    '''
    Template out a file and save to dest_file 
    - src_file should be relative to the template_dir
    - dest_file should be full path
    '''
    env = Environment(loader=FileSystemLoader(template_dir))
    print("writing {} to {}".format(src_file, dest_file))
    template = env.get_template(src_file)
    with open('{}'.format(dest_file), "w") as file:
        file.write(template.render(input_data))

