import sys
sys.path.append('lib')
import deployer
import os
import argparse
import yaml


project_name = 'tapis'
basedir = os.path.dirname(os.path.realpath(__file__))
print(basedir)

parser = argparse.ArgumentParser(description="Generate directory structure of Tapis deployment files from templates.")

parser.add_argument('--input', nargs='?',type=argparse.FileType('r'), help="File location of yaml config")

args = parser.parse_args()

input_data = yaml.safe_load(args.input)


deployer.jinjatest(input_data)