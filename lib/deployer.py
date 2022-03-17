import os
from unittest import result
from jinja2 import Environment, FileSystemLoader, StrictUndefined

def mkdir_if_missing(dir):
    '''
    Create dir if it does not exist
    '''
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_all_components_in_path(p):
    """
    Return all the components in a path, p, as a python list.
    Ex: get_all_components_in_path('/a/b/c') returns ['a', 'b', 'c']
        get_all_components_in_path('/a/b/c/) returns ['a', 'b', 'c']
    """
    result = []
    while True:        
        if not p or p == '/':
            return result
        head, tail = os.path.split(p)
        if tail:
            result.append(tail)
        if head == '/':
            return result
        p = head


def template_dirs_files(template_dir, components):
    """
    Returns all the template directories and files that need to be created and compiled for 
    a specific tapis site. It uses the `components` parameter to check whether a directory 
    or file needs to be includes.
    """
    template_dirs = []
    template_files = []

    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(template_dir)):
        for d in dirnames:
            full_dir = os.path.join(dirpath, d)
            # check if the full_dir is a subdirectory of the components to include
            for c in components:
                # if we find a component in the full_dir, we need to process it
                if c in get_all_components_in_path(full_dir):
                    template_dirs.append(full_dir)
                    break
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            # we always add all files in the root directory --
            if dirpath == template_dir:
                template_files.append(full_path)
                continue
            # for any file in a subdirectory, check if the full_path is a subdirectory of the 
            # components to include
            for c in components:
                # if we find a component in the full_path, we need to process it
                if c in get_all_components_in_path(full_path):
                    template_files.append(full_path)
                    break
    return template_dirs, template_files
 

def copy_dir_tree(template_dir, dest_dir_base, template_dirs):
    '''
    Create necessary Tapis deployment directory structure.
    '''

    print('Creating Tapis directory tree from templates.')
    for i in template_dirs:
        # replace template path with dest_dir_base
        dest_dir = str(i).replace(template_dir, dest_dir_base)
        # uncomment to debug
        #print('{} -> {}'.format(i,dest_dir))
        print(f"creating directory: {dest_dir}")
        mkdir_if_missing(dest_dir)


def copy_files_tree(template_dir, dest_dir_base, input_data, template_files):
    '''
    Compile deployment templates to the destination directory.
    '''
    print('Creating Tapis files from templates.')
    for i in template_files:
        # save permissions from template file
        permissions = os.stat(i)[0]
        # replace template path with dest_dir_base
        dest_file = str(i).replace(template_dir, dest_dir_base)
        # remove template_dir path prefix from i
        relative_i = str(i).replace(template_dir, '')
        # debug
        # uncomment to debug
        #print('{} -> {}'.format(i,dest_file))
        apply_template(template_dir, relative_i, dest_file, input_data)
        # apply same permissions from template file
        os.chmod(dest_file, permissions)

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

