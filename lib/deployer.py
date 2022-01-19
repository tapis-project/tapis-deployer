import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined

def mkdir_if_missing(dir):
    '''
    Create dir if it does not exist
    '''
    if not os.path.exists(dir):
        os.mkdir(dir)

def copy_dir_tree(template_dir, dest_dir_base, exclude_subdirs):
    '''
    Walk through the template directory and create Tapis deployment files from templates. 
    Skip the dirs/components in "exclude" list.
    '''

    print('Creating Tapis directory tree from templates.')

    # recreate template dir directory structure recursively

    template_dirs = [dest_dir_base]

    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(template_dir)):
        for d in dirnames:
            #print(os.path.join(dirpath,d))
            template_dirs.append(os.path.join(dirpath,d))

    for i in template_dirs:
        # replace template path with dest_dir_base
        dest_dir = str(i).replace(template_dir, dest_dir_base)
        # uncomment to debug
        #print('{} -> {}'.format(i,dest_dir))
        mkdir_if_missing(dest_dir)

def copy_files_tree(template_dir, dest_dir_base, input_data, exclude_subdirs):
    '''
    Walk through the template directory and create Tapis deployment files from templates. 
    Skip the dirs/components in "exclude" list.
    '''

    print('Creating Tapis files from templates.')

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
        # uncomment to debug
        #print('{} -> {}'.format(i,dest_file))
        apply_template(template_dir, relative_i, dest_file, input_data)



def apply_template(template_dir, src_file, dest_file, input_data):
    '''
    Template out a file and save to dest_file 
    - src_file should be relative to the template_dir
    - dest_file should be full path
    '''
    env = Environment(loader=FileSystemLoader(template_dir))
    # uncomment to debug
    #print("writing {} to {}".format(src_file, dest_file))
    template = env.get_template(src_file)
    with open('{}'.format(dest_file), "w") as file:
        file.write(template.render(input_data))

