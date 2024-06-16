import argparse
import sys
from build_datapack import *

isCompiled = getattr(sys, 'frozen', False)
isUsingDefaults = (len(sys.argv) < 2)
validLootTableList = ['fishing', 'village', 'mansion', 'stronghold', 'zombie']
greeting = "Babel Book Loot Generator, v1.0%s" % (' (Windows)' if isCompiled else '')

def restricted_float(x):
    error = "%r not a value between 0.0 and 1.0"
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(error % x)

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(error % x)
    return x

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Optional output zip filename. (default: %(default)s)', nargs='?', default='babel.zip')
parser.add_argument('-v', '--version', action='version', version=greeting)
parser.add_argument('-d', dest="loottable", default=[], action='append', choices=validLootTableList,
                    help='Disable adding books to the given loot tables. Can be repeated to disable more than one.')
# parser.add_argument('--gen2', action='store', type=restricted_float, default=0.3, metavar="CHANCE",
                    # help="Chance a book will be marked as a 'Copy of a copy', between 0.0 and 1.0. (default: %(default)s)")
# parser.add_argument('--gen1', action='store', type=restricted_float, default=0.01, metavar="CHANCE",
                    # help="Chance a book will be marked as a 'Copy of original', between 0.0 and 1.0. (default: %(default)s)")
# parser.add_argument('--gen0', action='store', type=restricted_float, default=0.003, metavar="CHANCE",
                    # help="Chance a book will be marked as an 'Original', between 0.0 and 1.0. (default: %(default)s)")
#parser.add_argument('-l', '--loottable', action='store_true',
                    # help="Don't build the datapack, instead just output the loot table. The default filename is books.json.")
parser.add_argument('-i', '--indent', help='Indent output JSON files.', action='store_true')
if isCompiled:
    parser.add_argument('-!', '--no-wait', action='store_true',
                        help="Don't wait for user input when finished. Triggered automatically by using any other argument.")
args = parser.parse_args()

if args.indent:
    indent = 4
else:
    indent = None

print("\n"+greeting)
print("="*len(greeting)+"\n")

if isUsingDefaults:
    print("Using default configuration, for more options try %s -h\n" % sys.argv[0])

try:
    from build_loottable import loottable
    print ("Found %d books." % len(loottable['pools'][0]['entries']))

    print ("Building datapack...")
    buildDatapack(args.filename, args.loottable, loottable, indent=indent)
    print ("\nDatapack build complete! Copy %s to your world's datapack directory." % args.filename)

except Exception as e:
    print("\nError: "+str(e))

finally:
    if isCompiled and isUsingDefaults:
        input("\nPress ENTER or close this window.")
