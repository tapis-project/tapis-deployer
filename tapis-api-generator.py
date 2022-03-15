import sys
import os
me=os.path.abspath(__file__)
medir=os.path.dirname(me)
melib=(medir+'/lib')
sys.path.append(melib)
import deployer
import argparse
import yaml

basedir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Generate directory structure of Tapis deployment files from templates.")

parser.add_argument('--destdir', required=True, help="Output destination directory")
parser.add_argument('--templatedir', default=medir+'/templates', help="Templates directory")
parser.add_argument('--input', type=argparse.FileType('r'), required=True, help="File location of yaml config")

args = parser.parse_args()

#template_dir = medir+'/templates'

# import yaml input file. do not need "open" because type is set by argparse
inpdata = yaml.safe_load(args.input)

# list of directories that deployer should compile for the site
compontents = inpdata.get('components_to_deploy')

# todo: test source dir
# todo: test dest dir

print(f"Running with {args.templatedir} template directory...")
print(f"Running with {compontents} components...")

template_dirs, template_files = deployer.template_dirs_files(args.templatedir, compontents)
template_dirs.append(args.destdir)
deployer.copy_dir_tree(args.templatedir, args.destdir, template_dirs)
deployer.copy_files_tree(args.templatedir, args.destdir, inpdata, template_files)

# deployer.copy_dir_tree(args.templatedir, args.destdir, compontents)
# deployer.copy_files_tree(args.templatedir, args.destdir, inpdata, compontents)
