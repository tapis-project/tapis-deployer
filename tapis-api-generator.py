import sys
sys.path.append('lib')
import deployer
import os
import argparse
import yaml

def main():

    project_name = 'tapis'
    basedir = os.path.dirname(os.path.realpath(__file__))
    print(basedir)

    parser = argparse.ArgumentParser(description="Generate yaml config file")
    parser.add_argument('input', metavar='inFile', nargs='?',type=argparse.FileType('r'), 
                        help="File location of yaml config")

    parser.add_argument('-o', dest='outDir', metavar='outDir', nargs='?',
                        help="File location of program output, if not specified defaults to tmp/tapis")

    args = parser.parse_args()
    if not args.input:
        parser.print_help()
        exit(1)

    outDir = args.outDir
    file_path = ""

    # import yaml input file. do not need "open" because type is set by argparse
    input_data = yaml.safe_load(args.input)

    # debug
    print(input_data)
    print(type(input_data))

# todo: create python testing env
# todo: test for duplicate vars
# todo: test to ensure top level of input_data is type dict



    # todo: reword? 
    tapis_dir = '{}/{}'.format(outDir, project_name)
    tapis_dir = os.path.expanduser(tapis_dir)
    if not os.path.exists(tapis_dir):
        os.makedirs(tapis_dir)
    deployer.create_tapis("templates", tapis_dir, input_data)

    #deployer.write_tapis(input_data, file_path, os.path.abspath(outDir))









if __name__ == '__main__':
    main()
