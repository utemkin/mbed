import sys
from os.path import join, abspath, dirname, exists
ROOT = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from shutil import move, rmtree
from os.path import join, exists, basename
from optparse import OptionParser

from workspace_tools.paths import EXPORT_DIR, EXPORT_WORKSPACE, EXPORT_TMP
from workspace_tools.paths import MBED_BASE, MBED_LIBRARIES
from workspace_tools.export import export, setup_user_prj, EXPORTERS
from workspace_tools.utils import args_error
from workspace_tools.tests import TESTS, Test, TEST_MAP
from workspace_tools.targets import TARGET_NAMES
try:
    import workspace_tools.private_settings as ps
except:
    ps = object()


if __name__ == '__main__':
    # Parse Options
    parser = OptionParser()

    targetnames = TARGET_NAMES
    targetnames.sort()
    toolchainlist = EXPORTERS.keys()
    toolchainlist.sort()

    parser.add_option("-m", "--mcu", metavar="MCU", default='LPC1768',
        help="generate project for the given MCU (%s)" % ', '.join(targetnames))

    parser.add_option("-i", dest="ide", default='uvision',
        help="The target IDE: %s" % str(toolchainlist))

    parser.add_option("-c", "--clean", action="store_true", default=False,
        help="clean the export directory")

    parser.add_option("-p", type="int", dest="program",
        help="The index of the desired test program: [0-%d]" % (len(TESTS)-1))

    parser.add_option("-n", dest="program_name",
        help="The name of the desired test program")

    parser.add_option("-b", dest="build", action="store_true", default=False,
        help="use the mbed library build, instead of the sources")

    parser.add_option("-L", "--list-tests", action="store_true", dest="list_tests", default=False, 
        help="list available programs in order and exit")

    (options, args) = parser.parse_args()


    # Print available tests in order and exit
    if options.list_tests is True:
        print '\n'.join(map(str, sorted(TEST_MAP.values())))
        sys.exit()

    # Clean Export Directory
    if options.clean:
        if exists(EXPORT_DIR):
            rmtree(EXPORT_DIR)

    # Target
    if options.mcu is None :
        args_error(parser, "[ERROR] You should specify an MCU")
    mcu = options.mcu

    # IDE
    if options.ide is None:
        args_error(parser, "[ERROR] You should specify an IDE")
    ide = options.ide

    # Program Number or name
    p, n = options.program, options.program_name

    if n is not None and p is not None:
        args_error(parser, "[ERROR] specify either '-n' or '-p', not both")
    if n:
        if not n in TEST_MAP.keys():
            # Check if there is an alias for this in private_settings.py
            if getattr(ps, "test_alias", None) is not None:
                alias = ps.test_alias.get(n, "")
                if not alias in TEST_MAP.keys():
                    args_error(parser, "[ERROR] Program with name '%s' not found" % n)
                else:
                    n = alias
            else:
                args_error(parser, "[ERROR] Program with name '%s' not found" % n)
        p = TEST_MAP[n].n
    if p is None or (p < 0) or (p > (len(TESTS)-1)):
        message = "[ERROR] You have to specify one of the following tests:\n"
        message += '\n'.join(map(str, sorted(TEST_MAP.values())))
        args_error(parser, message)

    # Project
    if p is None or (p < 0) or (p > (len(TESTS)-1)):
        message = "[ERROR] You have to specify one of the following tests:\n"
        message += '\n'.join(map(str, sorted(TEST_MAP.values())))
        args_error(parser, message)
    test = Test(p)

    if not options.build:
        # Substitute the library builds with the sources
        # TODO: Substitute also the other library build paths
        if MBED_LIBRARIES in test.dependencies:
            test.dependencies.remove(MBED_LIBRARIES)
            test.dependencies.append(MBED_BASE)

    # Build the project with the same directory structure of the mbed online IDE
    project_dir = join(EXPORT_WORKSPACE, test.id)
    setup_user_prj(project_dir, test.source_dir, test.dependencies)

    # Export to selected toolchain
    tmp_path, report = export(project_dir, test.id, ide, mcu, EXPORT_WORKSPACE, EXPORT_TMP)
    if report['success']:
        zip_path = join(EXPORT_DIR, "%s_%s_%s.zip" % (test.id, ide, mcu))
        move(tmp_path, zip_path)
        print "[OK]"
    else:
        print '[ERRROR] %s' % report['errormsg']
