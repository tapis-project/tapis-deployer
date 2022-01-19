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

# not working yet
#exclude=["files","jobs"]
exclude=[]

# todo: test source dir
# todo: test dest dir

deployer.copy_dir_tree(args.templatedir, args.destdir, exclude)
deployer.copy_files_tree(args.templatedir, args.destdir, inpdata, exclude)
