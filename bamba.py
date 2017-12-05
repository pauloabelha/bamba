import sys
from optparse import OptionParser
from standardize import action_standardize
from plot_pcl import plot_pcl
from plot_pcl import plot_pcl_from_file
from pcl_info import print_pcl_info
import superquadric as sq


ACTION_LIST = ['standardize', 'plot', 'info',
               'sample_superellipse', 'sample_superparabola', 'sample_superellipsoid',
               'sample_superparaboloid']
ACTIONS_THAT_REQUIRE_FILES = ['standardize', 'plot', 'info']

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
parser.add_option("-p", "--params", dest="params",
                  action="store", default='',
                  help="String containing a list of params (see manual)")
parser.add_option("-v", "--verbose", dest="verbose",
                  help="output information to stdout (default is false)", metavar="VERBOSE")

(options, args) = parser.parse_args()

parse_action(options.action_name)
action_name = options.action_name

batch_folder = parse_batch_folder(options.batch_folder)

if action_name in ACTIONS_THAT_REQUIRE_FILES:
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
    plot_pcl_from_file(input_filename, verbose)

if action_name == 'info':
    if verbose:
        print('Input file: ' + input_filename)
    print_pcl_info(input_filename)

if action_name == 'sample_superellipse':
    if len(options.params) == 0:
        print("Please specify the superellipse three params as a csv string (e.g. -p 2,1,0.5)")
        sys.exit(1)
    else:
        se_params = options.params.split(",")
        if not len(se_params) == 3:
            print("Superellipse sampling requires a list of exactly three params: a, b and epsilon1")
            sys.exit(1)
        a = float(se_params[0])
        b = float(se_params[1])
        eps1 = float(se_params[2])
    pcl = sq.sample_superellipse(a, b, eps1)
    plot_pcl(pcl, window_title="superellipse")

if action_name == 'sample_superparabola':
    if len(options.params) == 0:
        print("Please specify the superparabola three params as a csv string (e.g. -p 2,1,0.5)")
        sys.exit(1)
    else:
        sp_params = options.params.split(",")
        if not len(sp_params) == 3:
            print("Superparabola sampling requires a list of exactly three params: a, b and epsilon1")
            sys.exit(1)
        a = float(sp_params[0])
        b = float(sp_params[1])
        eps1 = float(sp_params[2])
    pcl = sq.sample_superparabola(a, b, eps1)
    plot_pcl(pcl, window_title="superparabola")

if action_name == 'sample_superellipsoid':
    if len(options.params) == 0:
        print("Please specify the superellipsoid's 5 params as a csv string (e.g. -p 1,2,3,0.1,1)")
        sys.exit(1)
    else:
        se_params = options.params.split(",")
        if not len(se_params) == 5:
            print("Superellipsoid sampling requires a list of exactly five params: a, b, c, epsilon1 and epsilon2")
            sys.exit(1)
    pcl = sq.sample_superellipsoid([float(x) for x in se_params], 2000)
    plot_pcl(pcl, window_title="superparabola")

if action_name == 'sample_superparaboloid':
    if len(options.params) == 0:
        print("Please specify the Superparaboloid's 11 params as a csv string")
        sys.exit(1)
    else:
        sp_params = options.params.split(",")
        if not len(sp_params) == 14:
            print("Superparaboloid sampling requires a list of exactly 14 params, but " + str(len(sp_params)) + " were given.")
            sys.exit(1)
    pcl = sq.sample_superparaboloid([float(x) for x in sp_params], 10000)
    plot_pcl(pcl, window_title="superparabola", color='k')
