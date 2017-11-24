import sys
from optparse import OptionParser
from standardize import action_standardize
from plot_pcl import plot_pcl

ACTION_LIST = ['standardize', 'plot']

def parse_action(action_name):
    if action_name is None:
        print('Action name cannot be None')
        parser.print_help()
        sys.exit(1)
    if action_name == '':
        print('Action name cannot be empty')
        parser.print_help()
        sys.exit(1)
    if not action_name in ACTION_LIST:
        print('Action ''' + action_name + ' not available')
        parser.print_help()
        sys.exit(1)
    return action_name

def parse_batch_folder(batch_folder):
    if batch_folder is None:
        print('Batch folder cannot be None')
        parser.print_help()
        sys.exit(1)
    return batch_folder

def parse_filename(filename):
    if filename is None:
        print('Filename cannot be None')
        parser.print_help()
        sys.exit(1)
    if filename == '':
        print('Filename cannot be empty')
        parser.print_help()
        sys.exit(1)
    if len(filename) < 5 or not filename[len(filename)-4:len(filename)] == '.ply':
        print('Please provide a PLY point cloud as input file')
        parser.print_help()
        sys.exit(1)
    return filename

def parse_verbose(verbose):
    if verbose is None:
        return False
    verbose = verbose.lower()
    if verbose == '':
        print('Verbose option cannot be empty')
        parser.print_help()
        sys.exit(1)
    if not (verbose == 'true' or verbose == 'false'):
        print('Verbose option can only have one of these two arguments: (true, false)')
        parser.print_help()
        sys.exit(1)
    if verbose == 'true':
        return True
    else:
        return False

parser = OptionParser(usage="%prog [-s] [-o] [-v]", version="%prog 1.0")
parser.add_option("-a", "--action", dest="action_name",
                  action="store", default='',
                  help="action to be performed: " + str(ACTION_LIST))
parser.add_option("-b", "--batch", dest="batch_folder",
                  action="store", default='',
                  help="folder in which to perform the action to all point clouds")
parser.add_option("-i", "--input", dest="input_filename",
                  action="store", default='',
                  help="PLY input point cloud file name")
parser.add_option("-o", "--output", dest="output_filename",
                  action="store", default='',
                  help="PLY output point cloud file name")
parser.add_option("-v", "--verbose", dest="verbose",
                  help="output information to stdout (default is false)", metavar="VERBOSE")

(options, args) = parser.parse_args()

parse_action(options.action_name)
action_name = options.action_name

batch_folder = parse_batch_folder(options.batch_folder)

input_filename = parse_filename(options.input_filename)

default_output_file_name = options.input_filename
if options.output_filename == '':
    output_filename = default_output_file_name
else:
    output_filename = options.output_filename
output_filename = parse_filename(output_filename)

verbose = parse_verbose(options.verbose)

if verbose:
    print('Action: ' + action_name)

if action_name == 'standardize':
    if batch_folder == '':
        if verbose:
            print('Input file: ' + input_filename)
            print('Output file: ' + output_filename)
        action_standardize(input_filename, output_filename, verbose)
    else:
        if verbose:
            print('Processing batch folder: ' + batch_folder)
            print('Output files will be saved to ' + batch_folder + 'standardized/')

if action_name == 'plot':
    if verbose:
        print('Input file: ' + input_filename)
    plot_pcl(input_filename, verbose)